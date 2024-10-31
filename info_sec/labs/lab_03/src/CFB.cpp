//
// Created by nikitalystsev on 26.10.2024.
//

#include "CFB.h"

#include <utility>
#include <fstream>

CFB::CFB(AES aes, const vector<uint8_t> &iv) : _aes{std::move(aes)}, _iv{iv} {

}

string CFB::encryptString(const string &str, const string &key) {
    this->_resetDiffSize();

    vector<uint8_t> vUint8Str(str.begin(), str.end());
    vector<uint8_t> vUint8Key(key.begin(), key.end());

    vector<vector<uint8_t>> strAsBlocks = CFB::_msgToBlocks(vUint8Str);

    vector<uint8_t> encryptedStr = this->_encrypt(strAsBlocks, vUint8Key);

    return string{encryptedStr.begin(), encryptedStr.end()};
}

string CFB::decryptString(const string &str, const string &key) {
    vector<uint8_t> vUint8Str(str.begin(), str.end());
    vector<uint8_t> vUint8Key(key.begin(), key.end());

    vector<vector<uint8_t>> strAsBlocks = CFB::_msgToBlocks(vUint8Str);

    vector<uint8_t> encryptedStr = this->_decrypt(strAsBlocks, vUint8Key);

    return string{encryptedStr.begin(), encryptedStr.end()};
}

void CFB::encryptFile(const string &filepath, const string &outFilepath, const string &key) {
    this->_resetDiffSize();

    ofstream outputFile(outFilepath, ios::binary);
    if (!outputFile.is_open()) {
        cout << "out file dont open" << endl;
        return;
    }

    vector<uint8_t> data = CFB::_getUint8BytesFromFile(filepath);
    vector<uint8_t> vUint8Key(key.begin(), key.end());

    vector<vector<uint8_t>> binData = CFB::_msgToBlocks(data);

    vector<uint8_t> encryptedData = this->_encrypt(binData, vUint8Key);

    for (auto encByte: encryptedData) {
        char tmp = static_cast<char>(encByte);
        outputFile.put(tmp);
    }

    outputFile.close();
}

void CFB::decryptFile(const string &filepath, const string &outFilepath, const string &key) {
    ofstream outputFile(outFilepath, ios::binary);
    if (!outputFile.is_open()) {
        cout << "out file dont open" << endl;
        return;
    }

    vector<uint8_t> data = CFB::_getUint8BytesFromFile(filepath);
    vector<uint8_t> vUint8Key(key.begin(), key.end());

    vector<vector<uint8_t>> binData = CFB::_msgToBlocks(data);

    vector<uint8_t> encryptedData = this->_decrypt(binData, vUint8Key);

    for (auto encByte: encryptedData) {
        char tmp = static_cast<char>(encByte);
        outputFile.put(tmp);
    }

    outputFile.close();
}

vector<uint8_t> CFB::_encrypt(const vector<vector<uint8_t>> &blocks, const vector<uint8_t> &key) {
    vector<uint8_t> ci = this->_iv;

    vector<uint8_t> result;

    for (const vector<uint8_t> &block: blocks) {
        vector<uint8_t> tmp = this->_aes.encryptBlock(ci, key);

        ci = CFB::_xorTwoBlocks(block, tmp);

        result.insert(result.end(), ci.begin(), ci.end());
    }

    return result;
}

vector<uint8_t> CFB::_decrypt(const vector<vector<uint8_t>> &blocks, const vector<uint8_t> &key) {
    vector<uint8_t> ci = this->_iv;

    vector<uint8_t> result;

    for (const vector<uint8_t> &block: blocks) {
        vector<uint8_t> tmp = this->_aes.encryptBlock(ci, key);

        ci = CFB::_xorTwoBlocks(block, tmp);

        result.insert(result.end(), ci.begin(), ci.end());

        ci = block;
    }

    this->_truncateByCurrDiffSize(result);

    return result;
}

vector<uint8_t> CFB::_xorTwoBlocks(const vector<uint8_t> &block1, const vector<uint8_t> &block2) {
    vector<uint8_t> result(block1.size());

    for (int i = 0; i < block1.size(); i++) {
        result[i] = block1[i] ^ block2[i];
    }

    return result;
}

vector<vector<uint8_t>> CFB::_msgToBlocks(const vector<uint8_t> &msg) {
    int numArrays = static_cast<int>(msg.size()) / 16;
    int remainder = static_cast<int>(msg.size()) % 16;

    vector<vector<uint8_t>> arrBlocks;
    for (int i = 0; i < numArrays; ++i) {
        vector<uint8_t> subArray(msg.begin() + i * 16, msg.begin() + (i + 1) * 16);
        arrBlocks.push_back(subArray);
    }

    if (remainder > 0) {
        vector<uint8_t> subArray(msg.end() - remainder, msg.end());

        size_t padding = 16 - (msg.size() % 16);

        this->_diffSize = static_cast<int>(padding);

        for (size_t i = 0; i < padding; ++i) {
            subArray.push_back(static_cast<uint8_t>(0));
        }

        arrBlocks.push_back(subArray);
    }

    return arrBlocks;
}

vector<uint8_t> CFB::_getUint8BytesFromFile(const string &filepath) {
    vector<uint8_t> result;

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

void CFB::_truncateByCurrDiffSize(vector<uint8_t> &msg) const {
    for (int i = 0; i < this->_diffSize; i++) {
        msg.pop_back();
    }
}

void CFB::_resetDiffSize() {
    this->_diffSize = 0;
}
