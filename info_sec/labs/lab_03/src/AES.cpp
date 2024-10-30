//
// Created by nikitalystsev on 26.10.2024.
//

#include <algorithm>
#include "AES.h"

void printMatrix(const vector<vector<uint8_t>> &matrix);

void print3DMatrix(const vector<vector<vector<uint8_t>>> &matrix);

AES::AES(int nb, int nk, int nr) :
        _nb{nb}, _nk{nk}, _nr{nr} {

}

/*
 * input -- 128 бит (4 слова -- 1 слово 32 бита)
 * key -- или 128, или 192, или 256 бит
 */
vector<uint8_t> AES::encryptBlock(const vector<uint8_t> &input, const vector<uint8_t> &key) {
    // копируем input в state
    vector<vector<uint8_t>> state = this->_inputToState(input);
    /*
     * Генерация ключей раунда.
     * Каждый ключ раунда имеет те же размеры, что и state
     */
    vector<vector<vector<uint8_t>>> roundKeys = this->_keyExpansion(key);
    // добавляем изначальный ключ к state
    AES::_addRoundKey(state, roundKeys[0]);

    // цикл по раундам шифрования (кроме последнего)
    for (int i = 1; i < this->_nr; i++) {
        this->_subBytes(state);
        AES::_shiftRows(state);
        AES::_mixColumns(state);
        AES::_addRoundKey(state, roundKeys[i]);
    }

    // последний раунд отдельно
    this->_subBytes(state);
    AES::_shiftRows(state);
    AES::_addRoundKey(state, roundKeys[roundKeys.size() - 1]);

    // матрицу обратно в блок
    return this->_stateToOutput(state);
}

vector<uint8_t> AES::decryptBlock(const vector<uint8_t> &encryptInput, const vector<uint8_t> &key) {
    // копируем input в state
    vector<vector<uint8_t>> state = this->_inputToState(encryptInput);
    /*
     * Генерация ключей раунда.
     * Каждый ключ раунда имеет те же размеры, что и state
     */
    vector<vector<vector<uint8_t>>> roundKeys = this->_keyExpansion(key);
    // добавляем последний ключ к state
    AES::_addRoundKey(state, roundKeys[roundKeys.size() - 1]);

    // цикл по раундам шифрования (кроме последнего)
    for (int i = this->_nr - 1; i > 0; i--) {
        AES::_invShiftRows(state);
        this->_invSubBytes(state);
        AES::_addRoundKey(state, roundKeys[i]);
        AES::_invMixColumns(state);
    }

    // последний раунд отдельно
    AES::_invShiftRows(state);
    AES::_invSubBytes(state);
    AES::_addRoundKey(state, roundKeys[0]);

    // матрицу обратно в блок
    return this->_stateToOutput(state);
}

vector<vector<uint8_t>> AES::_inputToState(const vector<uint8_t> &input) const {
    vector<vector<uint8_t>> state(4, vector<uint8_t>(this->_nb));

    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < this->_nb; c++) {
            state[r][c] = input[r + 4 * c];
        }
    }

    return state;
}

vector<uint8_t> AES::_stateToOutput(const vector<vector<uint8_t>> &state) const {
    vector<uint8_t> output(16);

    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < this->_nb; c++) {
            output[r + 4 * c] = state[r][c];
        }
    }

    return output;
}

vector<vector<vector<uint8_t>>> AES::_keyExpansion(const vector<uint8_t> &key) {
    vector<vector<uint8_t>> keyAsMtrWords = this->_keyToMtrWords(key);

    // тупо заполняю первые nk слов
    vector<vector<uint8_t>> resultWords(this->_nb * (this->_nr + 1), vector<uint8_t>(this->_nb));
    for (int i = 0; i < keyAsMtrWords.size(); i++) {
        resultWords[i] = keyAsMtrWords[i];
    }


    for (int i = this->_nk; i < this->_nb * (this->_nr + 1); i++) {
        vector<uint8_t> tmpWord = resultWords[i - 1];

        if (i % this->_nk == 0) {
            auto tmp = this->_subWord(AES::_rotWord(tmpWord));
            tmpWord = AES::_xorWordAndRcon(tmp, this->_rcon[i / this->_nk]);
        } else if (this->_nk > 6 and i % this->_nk == 4) {
            tmpWord = this->_subWord(tmpWord);
        }

        resultWords[i] = AES::_xorTwoWords(resultWords[i - this->_nk], tmpWord);
    }

    return this->_convertVecWordsToVecRoundKeys(resultWords);
}

void AES::_addRoundKey(vector<vector<uint8_t>> &state, const vector<vector<uint8_t>> &roundKey) {
    for (int i = 0; i < state.size(); ++i) {
        for (int j = 0; j < state[0].size(); ++j) {
            state[i][j] ^= roundKey[i][j];
        }
    }
}

void AES::_subBytes(vector<vector<uint8_t>> &state) {
    for (int i = 0; i < state.size(); ++i) {
        for (int j = 0; j < state[0].size(); ++j) {
            state[i][j] = this->_sbox[state[i][j]];
        }
    }
}

void AES::_invSubBytes(vector<vector<uint8_t>> &state) {
    for (int i = 0; i < state.size(); ++i) {
        for (int j = 0; j < state[0].size(); ++j) {
            state[i][j] = this->_invSbox[state[i][j]];
        }
    }
}

void AES::_shiftRows(vector<vector<uint8_t>> &state) {
    for (int i = 1; i < state.size(); ++i) {
        std::rotate(state[i].begin(), state[i].begin() + i, state[i].end());
    }
}

void AES::_invShiftRows(vector<vector<uint8_t>> &state) {
    for (int i = 1; i < state.size(); ++i) {
        std::rotate(state[i].rbegin(), state[i].rbegin() + i, state[i].rend());
    }
}

void AES::_mixColumns(vector<vector<uint8_t>> &state) {
    for (size_t i = 0; i < 4; ++i) {
        uint8_t s0 = state[0][i];
        uint8_t s1 = state[1][i];
        uint8_t s2 = state[2][i];
        uint8_t s3 = state[3][i];

        state[0][i] = AES::GMul(s0, 0x02) ^ AES::GMul(s1, 0x03) ^ s2 ^ s3;
        state[1][i] = s0 ^ AES::GMul(s1, 0x02) ^ AES::GMul(s2, 0x03) ^ s3;
        state[2][i] = s0 ^ s1 ^ AES::GMul(s2, 0x02) ^ AES::GMul(s3, 0x03);
        state[3][i] = AES::GMul(s0, 0x03) ^ s1 ^ s2 ^ AES::GMul(s3, 0x02);
    }
}

void AES::_invMixColumns(vector<vector<uint8_t>> &state) {
    for (size_t i = 0; i < 4; ++i) {
        uint8_t s0 = state[0][i];
        uint8_t s1 = state[1][i];
        uint8_t s2 = state[2][i];
        uint8_t s3 = state[3][i];

        state[0][i] = AES::GMul(s0, 0x0E) ^ AES::GMul(s1, 0x0B) ^ AES::GMul(s2, 0x0D) ^ AES::GMul(s3, 0x09);
        state[1][i] = AES::GMul(s0, 0x09) ^ AES::GMul(s1, 0x0E) ^ AES::GMul(s2, 0x0B) ^ AES::GMul(s3, 0x0D);
        state[2][i] = AES::GMul(s0, 0x0D) ^ AES::GMul(s1, 0x09) ^ AES::GMul(s2, 0x0E) ^ AES::GMul(s3, 0x0B);
        state[3][i] = AES::GMul(s0, 0x0B) ^ AES::GMul(s1, 0x0D) ^ AES::GMul(s2, 0x09) ^ AES::GMul(s3, 0x0E);
    }
}

vector<uint8_t> AES::_subWord(const vector<uint8_t> &word) {
    vector<uint8_t> result(word.size());

    for (int i = 0; i < word.size(); ++i) {
        result[i] = this->_sbox[word[i]];
    }

    return result;
}

/*
 * циклический сдвиг влево на 1 позицию
 */
vector<uint8_t> AES::_rotWord(const vector<uint8_t> &word) {
    vector<uint8_t> result = word;

    uint8_t temp = result[0];
    for (size_t i = 0; i < word.size() - 1; ++i) {
        result[i] = result[i + 1];
    }

    result[word.size() - 1] = temp;

    return result;
}


vector<vector<uint8_t>> AES::_keyToMtrWords(const vector<uint8_t> &key) const {
    vector<vector<uint8_t>> mtrWords(_nk, vector<uint8_t>(4));

    for (int i = 0; i < this->_nk; ++i) {
        for (int j = 0; j < 4; ++j) {
            mtrWords[i][j] = key[i * 4 + j];
        }
    }

    return mtrWords;
}

vector<uint8_t> AES::_xorWordAndRcon(const vector<uint8_t> &word, array<uint8_t, 4> rcon) {
    vector<uint8_t> result(word.size());

    for (int i = 0; i < word.size(); i++) {
        result[i] = word[i] ^ rcon[i];
    }

    return result;
}

vector<uint8_t> AES::_xorTwoWords(const vector<uint8_t> &word1, const vector<uint8_t> &word2) {
    vector<uint8_t> result(word1.size());

    for (int i = 0; i < word1.size(); i++) {
        result[i] = word1[i] ^ word2[i];
    }

    return result;
}

vector<vector<vector<uint8_t>>> AES::_convertVecWordsToVecRoundKeys(vector<vector<uint8_t>> vecWords) const {
    vector<vector<vector<uint8_t>>> result(
            this->_nr + 1,
            vector<vector<uint8_t>>(
                    4,
                    vector<uint8_t>(this->_nb)
            )
    );

    for (int i = 0; i < this->_nr + 1; ++i) {
        for (int j = 0; j < 4; ++j) {
            result[i][j] = vecWords[i * 4 + j];
        }
    }

//    print3DMatrix(result);

    return result;
}

uint8_t AES::GMul(uint8_t x, uint8_t y) {
    uint8_t result = 0;
    uint8_t hbit = 0;

    for (int i = 0; i < 8; ++i) {
        if (y & 1) {
            result ^= x;
        }
        hbit = x & 0x80;
        x <<= 1;
        if (hbit) {
            x ^= 0x1B;
        }
        y >>= 1;
    }

    return result;
}

void printMatrix(const vector<vector<uint8_t>> &matrix) {
    for (const auto &row: matrix) {
        for (auto byte: row) {
            cout << static_cast<int>(byte) << " ";
        }

        cout << endl;
    }
}

void print3DMatrix(const vector<vector<vector<uint8_t>>> &matrix) {
    for (const auto &mtr: matrix) {
        for (const auto &row: mtr) {
            for (auto byte: row) {
                cout << static_cast<int>(byte) << " ";
            }
            cout << endl;
        }
        cout << endl;
    }

}