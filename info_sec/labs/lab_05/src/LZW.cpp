//
// Created by nikitalystsev on 10.12.2024.
//

#include "LZW.h"

LZW::LZW(): _dict({}) {
    this->_dict.root = new TrieNode();
}

LZW::~LZW() {
    delete this->_dict.root;
}

pair<vector<uint8_t>, vector<uint8_t>> LZW::compressFile(const string &filename, const string &outputFilename) {
    vector<uint8_t> data = LZW::_getUint8BytesFromFile(filename);

    vector<uint8_t> compressedData = this->_compress(data);

    LZW::_writeData(outputFilename, compressedData);

    return {data, compressedData};
}

pair<vector<uint8_t>, vector<uint8_t>> LZW::decompressFile(const string &filename, const string &outputFilename) {
    vector<uint8_t> compressedData = LZW::_getUint8BytesFromFile(filename);

    vector<uint8_t> decompressedData = this->_decompress(compressedData);

    return {compressedData, decompressedData};
}

vector<uint8_t> LZW::_compress(const vector<uint8_t> &data) {
    LZW::_initDict(this->_dict);
    vector<uint8_t> result;

    vector<uint8_t> s; // текущая строка
    int nextIndex = 0;
    uint8_t nextByte;
    TrieNode* currNode = this->_dict.root;
    int code = 0xFF + 1;

    while (nextIndex < data.size()) {
        nextByte = data[nextIndex];
        if (currNode->children.contains(nextByte)) {
            currNode = &currNode->children[nextByte];
            nextIndex++;
        } else {
            result.push_back(currNode->code);
            currNode->children[nextByte].code = code;
            code++;
            currNode = this->_dict.root;
        }
    }

    if (currNode != this->_dict.root) {
        result.push_back(currNode->code);
    }

    return result;
}

vector<uint8_t> LZW::_decompress(const vector<uint8_t> &data) {
    LZW::_initDict(this->_dict);
    vector<uint8_t> result;

    vector<uint8_t> s; // текущая строка
    uint8_t prevCode = data[0];
    int nextIndex = 1;
    TrieNode* currNode = this->_dict.root;
    int code = 0xFF + 1;

    while (nextIndex < data.size()) {
        uint8_t currCode = data[nextIndex];
        cout << "currCode: " << currCode << endl;
        nextIndex++;

        if (currNode->children.contains(currCode)) {
            cout << "currNode contains currCode" << endl;
        }
//        if (currNode->children.contains(nextByte)) {
//            currNode = &currNode->children[nextByte];
//            nextIndex++;
//        } else {
//            result.push_back(currNode->code);
//            currNode->children[nextByte].code = code;
//            code++;
//            currNode = this->_dict.root;
//        }
    }

//    if (currNode != this->_dict.root) {
//        result.push_back(currNode->code);
//    }

    return result;
}

void LZW::_writeData(const string &outputFilename, const vector<uint8_t> &data) {
    ofstream outputFile(outputFilename, ios::binary);
    if (!outputFile.is_open()) {
        cout << "out file dont open" << endl;
        return ;
    }

    for (auto encByte: data) {
        char tmp = static_cast<char>(encByte);
        outputFile.put(tmp);
    }

    outputFile.close();
}

vector<uint8_t> LZW::_getUint8BytesFromFile(const string &filepath) {
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

void LZW::_initDict(TrieTree &dict) {
    dict.root->code = 0;

    for (int i = 0x00; i <= 0xFF; i++) {
        dict.root->children[i].code = i;
        dict.root->children[i].children.clear();
    }
}
