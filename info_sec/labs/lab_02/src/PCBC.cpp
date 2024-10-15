//
// Created by nikitalystsev on 15.10.2024.
//

#include "PCBC.h"
#include <algorithm>

PCBC::PCBC() : _iv(LONG_MAX) {

}

PCBC::PCBC(bitset<64> &iv) : _iv(iv) {

}

string PCBC::encryptString(const string &str, const string &key) {
    vector<char> vcharStr(str.begin(), str.end());
    vector<char> vcharKey(key.begin(), key.end());


    return string{result.begin(), result.end()};
}


bitset<64> PCBC::_vcharToBitset64(vector<char> input) {
    bitset<64> val;

    reverse(input.begin(), input.end());

    for (auto sym: input) {
        val <<= 8;
        bitset<8> tmp = sym;

        for (int i = 0; i < 8; i++) {
            val[i] = tmp[7 - i];
        }
    }

    return val;
}

vector<char> PCBC::_bitset64ToVchar(bitset<64> input) {
    vector<char> val = {};

    for (int i = 0; i < 64; i += 8) {
        char tmp = 0;
        for (int j = i; j < i + 8; j++) {
            tmp <<= 1;
            tmp |= input[j];
        }

        val.push_back(tmp);
    }

    return val;
}