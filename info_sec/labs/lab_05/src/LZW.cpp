//
// Created by nikitalystsev on 10.12.2024.
//

#include "LZW.h"


void printVector(const vector<uint16_t> &vec) {
//    cout << "vec.size() = " << vec.size() << endl;

    for (auto elem: vec) {
        cout << elem << " ";
    }
    cout << endl;
}

void printMtr(const vector<vector<uint16_t>> &mtr) {
    for (const auto& elem: mtr) {
        printVector(elem);
    }
}

LZW::LZW() : _dict(new TrieNode()) {
}

LZW::~LZW() = default;

pair<vector<uint16_t>, vector<uint16_t>> LZW::compressFile(const string &filename, const string &outputFilename) {
//    cout << "call compressFile" << endl;

    vector<uint16_t> data = LZW::_getUint8BytesFromFile(filename);

    vector<uint16_t> compressedData = this->_compress(data);

    LZW::_writeData(outputFilename, compressedData);

    return {data, compressedData};
}

pair<vector<uint16_t>, vector<uint16_t>> LZW::decompressFile(const string &filename, const string &outputFilename) {
    vector<uint16_t> compressedData = LZW::_getUint8BytesFromFile(filename);

    vector<uint16_t> decompressedData = this->_decompress(compressedData);

    LZW::_writeData(outputFilename, decompressedData);

    return {compressedData, decompressedData};
}

vector<uint16_t> LZW::_compress(const vector<uint16_t> &data) {
    cout << "call _compress" << endl;
    LZW::_initDict(this->_dict);

    vector<uint16_t> result;

    vector<uint16_t> s; // текущая строка

    for (uint16_t currByte: data) {
        cout << "maxCode = " << static_cast<int>(this->_dict.getMaxCode()) << endl;

        vector<uint16_t> tmp = s;
        tmp.push_back(currByte);
        if (this->_dict.contains(tmp)) {
            s = tmp;
        } else {
            uint16_t code = this->_dict.encode(s);
            result.push_back(code);
            this->_dict.insert(tmp);
            s = vector<uint16_t>(1, currByte);
        }
    }

    uint16_t code = this->_dict.encode(s);
    result.push_back(code);

    this->_dict.print();

    return result;
}

vector<uint16_t> LZW::_decompress(const vector<uint16_t> &data) {
    cout << "call _decompress" << endl;

    LZW::_initDict(this->_dict);
    vector<vector<uint16_t>> tmpKeys;
    LZW::_initVectorKeys(tmpKeys);
//    printMtr(tmpKeys);

    vector<uint16_t> result;

    vector<uint16_t> s; // текущая строка
    uint16_t prevCode = data[0];
    vector<uint16_t> entry = this->_getKeyByCode(tmpKeys, prevCode);

    result.insert(result.end(), entry.begin(), entry.end());

    for (int i = 1; i < data.size(); ++i) {
//        this->_dict.print();

        uint16_t currCode = data[i];
        cout << "currCode: " << currCode << endl;
        entry = this->_getKeyByCode(tmpKeys, currCode);
        cout << "entry: ";
        printVector(entry);
        result.insert(result.end(), entry.begin(), entry.end());

        uint16_t ch = entry[0];

        vector<uint16_t> tmp = {ch};
        vector<uint16_t> newEntry = this->_getKeyByCode(tmpKeys, prevCode);
        tmp.insert(tmp.begin(), newEntry.begin(), newEntry.end());
        cout << "tmp: ";
        printVector(tmp);

        this->_dict.insert(tmp);

        tmpKeys.push_back(tmp);

        prevCode = currCode;
    }

//    cout << "result: ";
//    printVector(result);

//    int nextIndex = 1;
//    TrieNode *currNode = this->_dict.getRoot();
//    int code = 0xFF + 1;
//
//    while (nextIndex < data.size()) {
//        uint16_t currCode = data[nextIndex];
//        cout << "currCode: " << currCode << endl;
//        nextIndex++;

//        if (searchTrie(*this->_dict.root, )) {
//            cout << "currNode contains currCode" << endl;
//        }
//
//        if (currNode->children.contains(some)) {
//
//        }
//        if (currNode->children.contains(nextByte)) {
//            currNode = &currNode->children[nextByte];
//            nextIndex++;
//        } else {
//            result.push_back(currNode->code);
//            currNode->children[nextByte].code = code;
//            code++;
//            currNode = this->_dict.root;
//        }
//    }

//    if (currNode != this->_dict.root) {
//        result.push_back(currNode->code);
//    }

    return result;
}

void LZW::_writeData(const string &outputFilename, const vector<uint16_t> &data) {
//    cout << "call _writeData" << endl;

    ofstream outputFile(outputFilename, ios::binary);
    if (!outputFile.is_open()) {
        cout << "out file dont open" << endl;
        return;
    }

    for (auto encByte: data) {
        char tmp = static_cast<char>(encByte);
        outputFile.put(tmp);
    }

    outputFile.close();
}

vector<uint16_t> LZW::_getUint8BytesFromFile(const string &filepath) {
    vector<uint16_t> result;

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
    dict.getRoot()->code = 0;
    dict.getRoot()->isKey = false;

    for (int i = 0x00; i <= 0xFF; i++) {
        dict.getRoot()->children[i].code = i;
        dict.getRoot()->children[i].isKey = true;
        dict.getRoot()->children[i].children.clear();
    }
}

void LZW::_initVectorKeys(vector<vector<uint16_t>> &keys) {
    for (int i = 0x00; i <= 0xFF; i++) {
        keys.emplace_back(1, i);
    }
}


vector<uint16_t> LZW::_getKeyByCode(const vector<vector<uint16_t>> &keys, uint16_t code) {
    cout << "call _getKeyByCode" << endl;

    vector<uint16_t> _key;

    for (const auto & key : keys) {
        uint16_t currCode = this->_dict.getCode(key);

        if (currCode == code) {
            cout << "here" << endl;
            _key = key;
        }
    }

    return _key;
}
