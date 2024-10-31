//
// Created by nikitalystsev on 26.10.2024.
//

#ifndef LAB_03_CFB_H
#define LAB_03_CFB_H

#include <filesystem>

#include "AES.h"

class CFB {

private:
    AES _aes;
    const vector<uint8_t> _iv;
    int _diffSize = 0; // сколько байт добавили в последнем шифруемом блоке (если он не полный)

private:
    vector<uint8_t> _encrypt(const vector<vector<uint8_t>> &blocks, const vector<uint8_t> &key);

    vector<uint8_t> _decrypt(const vector<vector<uint8_t>> &blocks, const vector<uint8_t> &key);

    static vector<uint8_t> _xorTwoBlocks(const vector<uint8_t> &block1, const vector<uint8_t> &block2);

    vector<vector<uint8_t>> _msgToBlocks(const vector<uint8_t> &msg);

    static vector<uint8_t> _getUint8BytesFromFile(const string &filepath);

    void _truncateByCurrDiffSize(vector<uint8_t> &msg) const;

    void _resetDiffSize();

public:
    CFB(AES aes, const vector<uint8_t> &iv);

    string encryptString(const string &str, const string &key);

    string decryptString(const string &str, const string &key);

    void encryptFile(const string &filepath, const string &outFilepath, const string &key);

    void decryptFile(const string &filepath, const string &outFilepath, const string &key);
};


#endif //LAB_03_CFB_H
