//
// Created by nikitalystsev on 15.10.2024.
//

#include "DES.h"


bitset<64> DES::encryptBlock(bitset<64> block, bitset<64> key) {
    // применение начальной перестановки
    bitset<64> IPBlock = this->_applyIP(block);

    // генерация ключей шифрования для каждого раунда
    vector<bitset<48>> roundKeys = this->_genRoundKeys(key);

    // разбиение блока на 2 части -- L_0 и R_0
    auto [Li, Ri] = DES::_iPBlockToL0R0(IPBlock);

    // 16 раундов шифрования
    for (auto roundKey: roundKeys) {
        pair<bitset<32>, bitset<32>> value = this->_roundEncrypt(Li, Ri, roundKey);
        Li = value.first;
        Ri = value.second;
    }

    // применение конечной перестановки
    return this->_applyIpInv(Li, Ri);
}

bitset<64> DES::decryptBlock(bitset<64> block, bitset<64> key) {
    // применение начальной перестановки (такая же)
    bitset<64> IPBlock = this->_applyIP(block);

    // генерация ключей шифрования для каждого раунда (реверс)
    vector<bitset<48>> roundKeys = this->_genRoundKeysForDecrypt(key);

    // разбиение блока на 2 части -- L_16 и R_16
    auto [Li, Ri] = DES::_iPBlockToL0R0(IPBlock);

    // 16 раундов шифрования
    for (auto roundKey: roundKeys) {
        pair<bitset<32>, bitset<32>> value = this->_roundDecrypt(Li, Ri, roundKey);
        Li = value.first;
        Ri = value.second;
    }

    // применение конечной перестановки
    return this->_applyIpInv(Li, Ri);
}


bitset<64> DES::_applyIP(bitset<64> block) {
    bitset<64> newBlock;

    int i = 0;

    for (auto ind: this->_ip) {
        newBlock[i] = block[ind - 1];
        i++;
    }

    return newBlock;
}

vector<bitset<48>> DES::_genRoundKeys(bitset<64> key) {
    vector<bitset<48>> keys;

    bitset<56> P1Key = this->_applyP1Ki(key);

    for (auto cntBitsForShift: this->_kiLeftShiftCnt) {
        bitset<56> tmp = P1Key;

        auto [C0, D0] = DES::_p1KeyToC0D0(tmp);

        C0 = DES::_applyCycleLeftShift(C0, cntBitsForShift);
        D0 = DES::_applyCycleLeftShift(D0, cntBitsForShift);

        for (int i = 0; i < 28; i++) {
            P1Key[i] = C0[i];
            P1Key[i + 27] = D0[i];
        }

        bitset<48> P2Key = this->_applyP2Ki(P1Key);

        keys.push_back(P2Key);
    }

    return keys;
}

bitset<56> DES::_applyP1Ki(bitset<64> key) {
    bitset<56> newKey;

    int i = 0;
    for (auto index: this->_p1Ki) {
        newKey[i] = key[index - 1];
        i++;
    }

    return newKey;
}

bitset<48> DES::_applyP2Ki(bitset<56> key) {
    bitset<48> newKey;

    int i = 0;
    for (auto index: this->_p2Ki) {
        newKey[i] = key[index - 1];
        i++;
    }

    return newKey;
}

pair<bitset<28>, bitset<28>> DES::_p1KeyToC0D0(bitset<56> p1Key) {
    bitset<28> C0, D0;

    for (int i = 0; i < 56; i++) {
        if (i < 28) {
            C0[i] = p1Key[i];
        } else {
            D0[i - 28] = p1Key[i];
        }
    }

    return pair<bitset<28>, bitset<28>>{C0, D0};
}

bitset<28> DES::_applyCycleLeftShift(bitset<28> value, int cntBitsForShift) {
    bitset<28> tmp = value;

    value <<= cntBitsForShift;

    for (int i = 28 - cntBitsForShift, j = 0; i < 28; i++, j++) {
        value[i] = tmp[j];
    }

    return value;
}

pair<bitset<32>, bitset<32>> DES::_iPBlockToL0R0(bitset<64> iPBlock) {
    bitset<32> L0 = {};
    bitset<32> R0 = {};

    for (int i = 0; i < 32; i++) {
        L0[i] = iPBlock[i];
        R0[i] = iPBlock[i + 32];
    }

    return pair<bitset<32>, bitset<32>>{L0, R0};
}

pair<bitset<32>, bitset<32>> DES::_roundEncrypt(bitset<32> Li_minus_1, bitset<32> Ri_minus_1, bitset<48> ki) {
    bitset<32> Li = Ri_minus_1;
    bitset<32> Ri = Li_minus_1 ^ this->_f(Ri_minus_1, ki);

    return pair<bitset<32>, bitset<32>>{Li, Ri};
}


pair<bitset<32>, bitset<32>> DES::_roundDecrypt(bitset<32> Li, bitset<32> Ri, bitset<48> ki) {
    bitset<32> Ri_minus_1 = Li;
    bitset<32> Li_minus_1 = Ri ^ this->_f(Li, ki);

    return pair<bitset<32>, bitset<32>>{Li_minus_1, Ri_minus_1};
}

bitset<32> DES::_f(bitset<32> Ri_minus_1, bitset<48> ki) {
    bitset<48> extendRi_minus_1 = this->_applyE(Ri_minus_1);
    bitset<48> xorRi_minus_1 = extendRi_minus_1 ^ ki;

    bitset<6> tmp = {};
    bitset<32> result = {};

    int k = 0;
    for (int i = 0; i < 8; i++) {
        // block of 6 bits
        for (int j = 0; j < 6; j++) {
            tmp[j] = xorRi_minus_1[i * 6 + j];
        }

        bitset<4> s_res = this->_applyS(tmp, i);

        for (int p = 0; p < 4; p++) {
            result[p + k] = s_res[p];
        }

        k += 4;
    }

    return this->_applyP(result);
}

bitset<48> DES::_applyE(bitset<32> Ri_minus_1) {
    bitset<48> newValue;

    int i = 0;
    for (auto index: this->_e) {
        newValue[i] = Ri_minus_1[index - 1];
        i++;
    }

    return newValue;
}

bitset<4> DES::_applyS(bitset<6> value, int i) {
    bitset<2> rowB = {};
    rowB[0] = value[0];
    rowB[1] = value[5];

    bitset<4> colB = {};
    colB[0] = value[1];
    colB[1] = value[2];
    colB[2] = value[3];
    colB[3] = value[4];

    auto row = rowB.to_ulong();
    auto col = colB.to_ulong();

    bitset<4> result = this->_s[i][row][col];

    return result;
}

bitset<32> DES::_applyP(bitset<32> value) {
    bitset<32> newValue;

    int i = 0;
    for (auto index: this->_p) {
        newValue[i] = value[index - 1];
        i++;
    }

    return newValue;
}

bitset<64> DES::_applyIpInv(bitset<32> Li, bitset<32> Ri) {
    bitset<64> tmpRes;

    for (int i = 0; i < 32; i++) {
        tmpRes[i] = Ri[i];
        tmpRes[i + 32] = Li[i];
    }

    int i = 0;
    bitset<64> result;
    for (auto index: this->_ipInv) {
        result[i] = tmpRes[index - 1];
        i++;
    }

    return result;
}

vector<bitset<48>> DES::_genRoundKeysForDecrypt(bitset<64> key) {
    vector<bitset<48>> roundKeys = this->_genRoundKeys(key);

    reverse(roundKeys.begin(), roundKeys.end());

    return roundKeys;
}
