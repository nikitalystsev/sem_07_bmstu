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
    uint16_t code;
    bool isKey;
    unordered_map<uint16_t, TrieNode> children;
};

class TrieTree {

private:
    TrieNode *_root;

private:
    uint16_t _getMaxCode(const TrieNode& node);

    void _getByCode(const TrieNode &node, uint16_t code, vector<uint16_t> &result);
public:
    explicit TrieTree(TrieNode *root);

    ~TrieTree();

    void setRoot(TrieNode *newRoot);

    TrieNode *getRoot();

    bool contains(const vector<uint16_t> &values);

    int getCode(const vector<uint16_t> &values);

    uint16_t encode(const vector<uint16_t>& values);

    void insert(const vector<uint16_t> &values);

    vector<uint16_t> getByCode(uint16_t code);

    uint16_t getMaxCode();

    void print();
};


#endif //LAB_05_TRIETREE_H
