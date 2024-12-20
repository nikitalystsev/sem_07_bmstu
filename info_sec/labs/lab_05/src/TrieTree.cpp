//
// Created by nikitalystsev on 14.12.2024.
//

#include "TrieTree.h"

TrieTree::TrieTree(TrieNode *root) : _root(root) {

}

TrieTree::~TrieTree() {
    delete this->_root;
}


void TrieTree::setRoot(TrieNode *newRoot) {
    this->_root = newRoot;
}

bool TrieTree::contains(const vector<uint8_t> &codes) {
//    cout << "call contains" << endl;

    if (!this->_root) return false;
    if (codes.empty()) return false;

    TrieNode *tmpRoot = this->_root;

    for (int i = 0; i < codes.size(); ++i) {
        if (!tmpRoot->children.contains(codes[i])) {
            return false;
        }

        if (i == codes.size() - 1) {
            if (!tmpRoot->children[codes[i]].isKey) return false;
        }

        tmpRoot = &tmpRoot->children[codes[i]];
    }

    return true;
}

void TrieTree::insert(const vector<uint8_t> &values) {
    if (!this->_root) return;
    if (values.empty()) return;

    TrieNode *tmpRoot = this->_root;

    for (int i = 0; i < values.size(); ++i) {
        if (!tmpRoot->children.contains(values[i])) {
            tmpRoot->children[values[i]].isKey = false;
        }

        if (i == values.size() - 1) {
            tmpRoot->children[values[i]].isKey = true;
            tmpRoot->children[values[i]].code = this->_getMaxCode(*this->_root) + 1;
        }

        tmpRoot = &(*tmpRoot).children[values[i]];
    }
}

void TrieTree::print() {
    stack<tuple<uint8_t, const TrieNode *, int>> stack;
    stack.emplace(0, this->_root, 0);

    while (!stack.empty()) {
        auto [key, val, depth] = stack.top();
        stack.pop();

        for (int i = 0; i < depth; ++i) cout << "  ";

        cout << "key: " << key;

        if (val->isKey) {
            cout << " Code: " << val->code << endl;
        } else cout << endl;

        for (const auto &pair: val->children) {
            stack.emplace(pair.first, &pair.second, depth + 1);
        }
    }
}

TrieNode *TrieTree::getRoot() {
    return this->_root;
}

int TrieTree::getCode(const vector<uint8_t> &values) {
    if (!this->_root) return -1;
    if (values.empty()) return -1;

    int code;

    TrieNode *tmpRoot = this->_root;

    for (int i = 0; i < values.size(); ++i) {
        if (!tmpRoot->children.contains(values[i])) {
            return -1;
        }

        if (i == values.size() - 1) {
            if (!tmpRoot->children[values[i]].isKey) return -1;

            code = tmpRoot->children[values[i]].code;
        }

        tmpRoot = &tmpRoot->children[values[i]];
    }

    return code;
}

uint32_t TrieTree::encode(const vector<uint8_t> &values) {
    return this->getCode(values);
}


uint32_t TrieTree::_getMaxCode(const TrieNode &node) {
    uint32_t maxCode = node.code;

    for (const auto &pair: node.children) {
        uint32_t childMaxCode = TrieTree::_getMaxCode(pair.second);
        maxCode = std::max(maxCode, childMaxCode);
    }

    return maxCode;
}

uint32_t TrieTree::getMaxCode() {
    return this->_getMaxCode(*this->_root);
}

