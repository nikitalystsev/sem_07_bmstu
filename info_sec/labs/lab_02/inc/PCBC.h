//
// Created by nikitalystsev on 15.10.2024.
//

#ifndef LAB_02_PCBC_H
#define LAB_02_PCBC_H

#include <vector>
#include <bitset>
#include "DES.h"

using namespace std;

class PCBC {
public:
    PCBC();
    explicit PCBC(bitset<64> &iv);
    string encryptString(const string& message, const string& key);
//    vector<char> cypher(vector<char> message, vector<char> key, bool decrypt=false);
//    vector<char> cypher(vector<char> message, vector<vector<char>> keys, bool decrypt=false);

private:
    static bitset<64> _vcharToBitset64(vector<char> input);

    static vector<char> _bitset64ToVchar(bitset<64> input);

    vector<bitset<64>> _getVector
    DES _des;

    const bitset<64> _iv;
};


#endif //LAB_02_PCBC_H
