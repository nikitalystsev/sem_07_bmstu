//
// Created by nikitalystsev on 15.10.2024.
//

#include "PCBC.h"


PCBC::PCBC(DES des, bitset<64> &iv) : _des(std::move(des)), _iv(iv) {

}

string PCBC::encryptString(const string &str, const string &key) {
    this->_diffSize = 0;
    vector<char> vCharStr(str.begin(), str.end());
    vector<char> vCharKey(key.begin(), key.end());

    vector<bitset<64>> strBlocks = PCBC::_getVBitset64FromVChar(vCharStr);
    bitset<64> bitsetKey = PCBC::_vCharToBitset64(vCharKey);

    vector<char> encryptedStr = this->_encrypt(strBlocks, bitsetKey);

    return string{encryptedStr.begin(), encryptedStr.end()};
}

string PCBC::decryptString(const string &str, const string &key) {
    vector<char> vCharStr(str.begin(), str.end());
    vector<char> vCharKey(key.begin(), key.end());

    vector<bitset<64>> strBlocks = PCBC::_getVBitset64FromVChar(vCharStr);
    bitset<64> bitsetKey = PCBC::_vCharToBitset64(vCharKey);

    vector<char> encryptedStr = this->_decrypt(strBlocks, bitsetKey);

    return string{encryptedStr.begin(), encryptedStr.end()};
}

void PCBC::encryptFile(const string &filepath, const string &outFilepath, const string &key) {
    this->_diffSize = 0;
    ofstream outputFile(outFilepath, ios::binary);
    if (!outputFile.is_open()) {
        cout << "out file dont open" << endl;
        return;
    }

    vector<char> data = this->_getCharBytesFromFile(filepath);
    vector<char> vCharKey(key.begin(), key.end());

    vector<bitset<64>> binData = PCBC::_getVBitset64FromVChar(data);
    bitset<64> bitsetKey = PCBC::_vCharToBitset64(vCharKey);

    vector<char> encryptedData = this->_encrypt(binData, bitsetKey);

    for (auto encByte: encryptedData) {
        outputFile.write(&encByte, sizeof(encByte));
    }

    outputFile.close();
}

void PCBC::decryptFile(const string &filepath, const string &outFilepath, const string &key) {
    ofstream outputFile(outFilepath, ios::binary);
    if (!outputFile.is_open()) {
        cout << "out file dont open" << endl;
        return;
    }

    vector<char> data = this->_getCharBytesFromFile(filepath);
    vector<char> vCharKey(key.begin(), key.end());

    vector<bitset<64>> binData = PCBC::_getVBitset64FromVChar(data);
    bitset<64> bitsetKey = PCBC::_vCharToBitset64(vCharKey);

    vector<char> encryptedData = this->_decrypt(binData, bitsetKey);

    for (auto encByte: encryptedData) {
        outputFile.write(&encByte, sizeof(encByte));
    }

    outputFile.close();
}

bitset<64> PCBC::_vCharToBitset64(vector<char> value) {
    bitset<64> val;

    reverse(value.begin(), value.end());

    for (auto sym: value) {
        val <<= 8;
        bitset<8> tmp = sym;

        for (int i = 0; i < 8; i++) {
            val[i] = tmp[7 - i];
        }
    }

    return val;
}

vector<char> PCBC::_bitset64ToVChar(bitset<64> value) {
    vector<char> val;

    for (int i = 0; i < 64; i += 8) {
        char tmp = 0;
        for (int j = i; j < i + 8; j++) {
            tmp <<= 1;
            tmp |= value[j];
        }

        val.push_back(tmp);
    }

    return val;
}

vector<bitset<64>> PCBC::_getVBitset64FromVChar(const vector<char> &value) {
    vector<char> buffer;

    vector<bitset<64>> result;

    for (auto symbol: value) {
        buffer.push_back(symbol);

        if (buffer.size() == 8) {
            result.push_back(PCBC::_vCharToBitset64(buffer));

            buffer.clear();
        }
    }

    if (!buffer.empty() && buffer.size() < 8) {
        while (buffer.size() < 8) {
            buffer.push_back((char) 0);
            this->_diffSize++;
        }

        result.push_back(PCBC::_vCharToBitset64(buffer));

        buffer.clear();
    }

    return result;
}

vector<char> PCBC::_encrypt(vector<bitset<64>> &strBlocks, bitset<64> &bitsetKey) {
    bitset<64> Ci_minus_1 = this->_iv;
    vector<char> encryptedStr;

    for (auto strBlock: strBlocks) {
        bitset<64> encryptBlock = this->_des.encryptBlock(Ci_minus_1 ^ strBlock, bitsetKey);

        vector<char> tmpRes = PCBC::_bitset64ToVChar(encryptBlock);

        for (auto symbol: tmpRes) {
            encryptedStr.push_back(symbol);
        }

        Ci_minus_1 = encryptBlock ^ strBlock;
    }

    return encryptedStr;
}

vector<char> PCBC::_decrypt(vector<bitset<64>> &strBlocks, bitset<64> &bitsetKey) {
    bitset<64> Ci_minus_1 = this->_iv;
    vector<char> decryptedStr;

    for (auto strBlock: strBlocks) {
        bitset<64> decryptedBlock = this->_des.decryptBlock(strBlock, bitsetKey);


        auto tmp = decryptedBlock ^ Ci_minus_1;

        vector<char> tmpRes = PCBC::_bitset64ToVChar(tmp);

        for (auto symbol: tmpRes) {
            decryptedStr.push_back(symbol);
        }

        Ci_minus_1 = tmp ^ strBlock;
    }

    cout << "diffSize = " << this->_diffSize << endl;

    if (this->_diffSize == 0) {
        return decryptedStr;
    }

    for (int i = 0; i < this->_diffSize; i++) {
        decryptedStr.pop_back();
    }

    return decryptedStr;
}

vector<char> PCBC::_getCharBytesFromFile(const string &filepath) {
    vector<char> result;

    ifstream file(filepath, ios::binary);
    if (!file.is_open()) {
        cout << "file dont open" << endl;
        return {};
    }

    size_t filesize = filesystem::file_size(filepath);
    size_t currByte = 0;

    while (currByte != filesize) {
        char byte;
        file.read(&byte, sizeof(byte));

        result.push_back(byte);

        currByte++;
    }

    file.close();

    return result;
}
