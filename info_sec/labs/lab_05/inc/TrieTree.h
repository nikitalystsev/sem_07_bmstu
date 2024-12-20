//
// Created by nikitalystsev on 14.12.2024.
//

#ifndef LAB_05_TRIETREE_H
#define LAB_05_TRIETREE_H

#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <filesystem>
#include <fstream>
#include <unordered_map>
#include <stack>

using namespace std;

struct TrieNode {
    uint32_t code;
    bool isKey;
    unordered_map<uint8_t, TrieNode> children;
};

class TrieTree {

private:
    TrieNode *_root;

private:
    uint32_t _getMaxCode(const TrieNode& node);

public:
    explicit TrieTree(TrieNode *root);

    ~TrieTree();

    void setRoot(TrieNode *newRoot);

    TrieNode *getRoot();

    bool contains(const vector<uint8_t> &values);

    int getCode(const vector<uint8_t> &values);

    uint32_t encode(const vector<uint8_t>& values);

    void insert(const vector<uint8_t> &values);

    uint32_t getMaxCode();

    void print();
};


#endif //LAB_05_TRIETREE_H
