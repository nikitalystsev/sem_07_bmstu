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

using namespace std;

// префиксное дерево для словарей
struct TrieNode {
    uint8_t code;
    unordered_map<uint8_t, TrieNode> children;
};

struct TrieTree {
    TrieNode *root;
};


class LZW {
private:
    TrieTree _dict;

private:
    static void _initDict(TrieTree &dict);

    static vector<uint8_t> _getUint8BytesFromFile(const string &filepath);

    vector<uint8_t> _compress(const vector<uint8_t> &data);

    vector<uint8_t> _decompress(const vector<uint8_t> &data);

    static void _writeData(const string &outputFilename, const vector<uint8_t> &data);

public:
    LZW();
    ~LZW();
    pair<vector<uint8_t>, vector<uint8_t>> compressFile(const string &filename, const string &outputFilename);
    pair<vector<uint8_t>, vector<uint8_t>> decompressFile(const string &filename, const string &outputFilename);
};


#endif //LAB_05_LZW_H
