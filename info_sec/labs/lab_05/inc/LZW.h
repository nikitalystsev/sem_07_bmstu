//
// Created by nikitalystsev on 10.12.2024.
//

#ifndef LAB_05_LZW_H
#define LAB_05_LZW_H


#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <filesystem>
#include <fstream>
#include <unordered_map>
#include <stack>
#include "TrieTree.h"

using namespace std;

class LZW {
private:
    TrieTree _dict;

private:
    static void _initDict(TrieTree &dict);
    static void _initVectorKeys(vector<vector<uint16_t>> &keys);

    static vector<uint16_t> _getUint8BytesFromFile(const string &filepath);

    vector<uint16_t> _compress(const vector<uint16_t> &data);

    vector<uint16_t> _decompress(const vector<uint16_t> &data);

    static void _writeData(const string &outputFilename, const vector<uint16_t> &data);

    vector<uint16_t> _getKeyByCode(const vector<vector<uint16_t>> &keys, uint16_t code);

public:
    LZW();

    ~LZW();

    pair<vector<uint16_t>, vector<uint16_t>> compressFile(const string &filename, const string &outputFilename);

    pair<vector<uint16_t>, vector<uint16_t>> decompressFile(const string &filename, const string &outputFilename);
};


#endif //LAB_05_LZW_H
