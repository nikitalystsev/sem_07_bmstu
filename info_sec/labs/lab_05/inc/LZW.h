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

    vector<uint32_t> codes;
private:
    static void _initDict(TrieTree &dict);

    static void _initVectorKeys(vector<vector<uint8_t>> &keys);

    static uint8_t _getBitsToRepresentInteger(uint32_t x);

    vector<uint8_t> _vec32ToVec8(const vector<pair<uint32_t, uint8_t>>& input);

    static uint32_t _readCode(const std::vector<uint8_t>& inputFile, int& bytesRead, uint8_t& bitsRead,uint8_t bitsToRead);

    static vector<uint8_t> _getUint8BytesFromFile(const string &filepath);

    vector<uint8_t> _compress(const vector<uint8_t> &data);

    vector<uint8_t> _decompress(const vector<uint8_t> &data);

    static void _writeData(const string &outputFilename, const vector<uint8_t> &data);

    vector<uint8_t> _getKeyByCode(const vector<vector<uint8_t>> &keys, uint32_t code);

public:
    LZW();

    ~LZW();

    pair<vector<uint8_t>, vector<uint8_t>> compressFile(const string &filename, const string &outputFilename);

    pair<vector<uint8_t>, vector<uint8_t>> decompressFile(const string &filename, const string &outputFilename);

};


#endif //LAB_05_LZW_H
