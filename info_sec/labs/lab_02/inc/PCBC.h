//
// Created by nikitalystsev on 15.10.2024.
//

#ifndef LAB_02_PCBC_H
#define LAB_02_PCBC_H

#include <vector>
#include <bitset>
#include <algorithm>
#include <utility>
#include "DES.h"

using namespace std;

class PCBC {
public:
    PCBC(DES des, bitset<64> &iv);

    string encryptString(const string &str, const string &key);
    string decryptString(const string &str, const string &key);

private:
    static bitset<64> _vCharToBitset64(vector<char> value);

    static vector<char> _bitset64ToVChar(bitset<64> value);

    static vector<bitset<64>> _getVBitset64FromVChar(const vector<char> &value);

    vector<char> _encrypt(vector<bitset<64>> &strBlocks, bitset<64> &bitsetKey);
    vector<char> _decrypt(vector<bitset<64>> &strBlocks, bitset<64> &bitsetKey);

    DES _des;
    const bitset<64> _iv;
};


#endif //LAB_02_PCBC_H
