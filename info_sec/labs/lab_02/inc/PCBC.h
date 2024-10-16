//
// Created by nikitalystsev on 15.10.2024.
//

#ifndef LAB_02_PCBC_H
#define LAB_02_PCBC_H

#include <vector>
#include <bitset>
#include <algorithm>
#include <utility>
#include <fstream>
#include <filesystem>
#include "DES.h"

using namespace std;

class PCBC {
public:
    PCBC(DES des, bitset<64> &iv);

    string encryptString(const string &str, const string &key);

    string decryptString(const string &str, const string &key);

    void encryptFile(const string &filepath, const string &outFilepath, const string &key);

    void decryptFile(const string &filepath, const string &outFilepath, const string &key);

private:
    static bitset<64> _vCharToBitset64(vector<char> value);

    static vector<char> _bitset64ToVChar(bitset<64> value);

    vector<bitset<64>> _getVBitset64FromVChar(const vector<char> &value);

    vector<char> _getCharBytesFromFile(const string &filepath);

    vector<char> _encrypt(vector<bitset<64>> &strBlocks, bitset<64> &bitsetKey);

    vector<char> _decrypt(vector<bitset<64>> &strBlocks, bitset<64> &bitsetKey);

    DES _des;
    const bitset<64> _iv;
    int _diffSize = 0; // сколько байт добавили в последнем шифруемом блоке (если он не полный)
};


#endif //LAB_02_PCBC_H
