//
// Created by nikitalystsev on 10.12.2024.
//

#include <thread>
#include "LZW.h"


void printVector(const vector<uint8_t> &vec) {
//    cout << "vec.size() = " << vec.size() << endl;

    for (auto elem: vec) {
        cout << elem << " ";
    }

    cout << endl;
}

void printMtr(const vector<vector<uint8_t>> &mtr) {
    for (const auto &elem: mtr) {
        printVector(elem);
    }
}

LZW::LZW() : _dict(new TrieNode()) {
}

LZW::~LZW() = default;

pair<vector<uint8_t>, vector<uint8_t>> LZW::compressFile(const string &filename, const string &outputFilename) {
//    cout << "call compressFile" << endl;

    vector<uint8_t> data = LZW::_getUint8BytesFromFile(filename);

    vector<uint8_t> compressedData = this->_compress(data);

    LZW::_writeData(outputFilename, compressedData);

    return {data, compressedData};
}

pair<vector<uint8_t>, vector<uint8_t>> LZW::decompressFile(const string &filename, const string &outputFilename) {
    cout << "call decompressFile" << endl;

    vector<uint8_t> compressedData = LZW::_getUint8BytesFromFile(filename);

    vector<uint8_t> decompressedData = this->_decompress(compressedData);

    LZW::_writeData(outputFilename, decompressedData);

    return {compressedData, decompressedData};
}

vector<uint8_t> LZW::_compress(const vector<uint8_t> &data) {
//    cout << "call _compress" << endl;
    LZW::_initDict(this->_dict);

//    cout << "data.size() = " << data.size() << endl;

    vector<pair<uint32_t, uint8_t>> tmpResult;

    vector<uint8_t> s; // текущая строка

    int i = 0;
    for (uint8_t currByte: data) {
//        cout << "compress iteration number: " << i << endl;

        vector<uint8_t> tmp = s;
        tmp.push_back(currByte);

        if (this->_dict.contains(tmp)) {
            s = tmp;
        } else {
            uint32_t code = this->_dict.encode(s);
//            cout << "code: " << code << endl;
            tmpResult.emplace_back(code, LZW::_getBitsToRepresentInteger(code));
            this->_dict.insert(tmp);
            s = vector<uint8_t>(1, currByte);
        }
        i++;
    }

    uint32_t code = this->_dict.encode(s);
//    cout << "code: " << code << endl;
    tmpResult.emplace_back(code, LZW::_getBitsToRepresentInteger(code));

//    cout << "tmpResult.size() = " << tmpResult.size() << endl;
//    this->_dict.print();

    return LZW::_vec32ToVec8(tmpResult);
}

vector<uint8_t> LZW::_decompress(const vector<uint8_t> &data) {
//    cout << "call _decompress" << endl;
    LZW::_initDict(this->_dict);
    vector<vector<uint8_t>> tmpKeys;
    LZW::_initVectorKeys(tmpKeys);

//    this->_dict.print();
//    cout << "compressed data size = " << data.size() << endl;

    vector<uint8_t> result;

    vector<uint8_t> s; // текущая строка

    uint32_t prevCode = codes[0];
    vector<uint8_t> entry = this->_getKeyByCode(tmpKeys, prevCode);
    result.insert(result.end(), entry.begin(), entry.end());

    for (int i = 1; i < data.size(); ++i) {
//        cout << "iteration number: " << i << endl;
//        this->_dict.print();

        uint32_t currCode = codes[i];
//        cout << "currCode: " << currCode << endl;
        entry = this->_getKeyByCode(tmpKeys, currCode);

        if (!entry.empty()) {
//            cout << "entry: ";
//            printVector(entry);
            result.insert(result.end(), entry.begin(), entry.end());

            uint8_t ch = entry[0];

            vector<uint8_t> tmp = {ch};
            vector<uint8_t> newEntry = this->_getKeyByCode(tmpKeys, prevCode);
            tmp.insert(tmp.begin(), newEntry.begin(), newEntry.end());
//            cout << "tmp: ";
//            printVector(tmp);

            this->_dict.insert(tmp);
            tmpKeys.push_back(tmp);

            prevCode = currCode;
        } else {
//            cout << "else branch" << endl;
            vector<uint8_t> oldEntry = this->_getKeyByCode(tmpKeys, prevCode);
            oldEntry.push_back(oldEntry[0]);

            result.insert(result.end(), oldEntry.begin(), oldEntry.end());

            this->_dict.insert(oldEntry);
            tmpKeys.push_back(oldEntry);

            prevCode = currCode;
        }

//        this->_dict.print();
    }

    return result;
}

void LZW::_writeData(const string &outputFilename, const vector<uint8_t> &data) {
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
    dict.getRoot()->code = 0;
    dict.getRoot()->isKey = false;

    for (int i = 0x00; i <= 0xFF; i++) {
        dict.getRoot()->children[i].code = i;
        dict.getRoot()->children[i].isKey = true;
        dict.getRoot()->children[i].children.clear();
    }
}

void LZW::_initVectorKeys(vector<vector<uint8_t>> &keys) {
    for (int i = 0x00; i <= 0xFF; i++) {
        keys.emplace_back(1, i);
    }
}


vector<uint8_t> LZW::_getKeyByCode(const vector<vector<uint8_t>> &keys, uint32_t code) {
//    cout << "call _getKeyByCode" << endl;

    vector<uint8_t> _key;

    for (const auto &key: keys) {
        uint32_t currCode = this->_dict.getCode(key);

        if (currCode == code) {
//            cout << "here" << endl;
            _key = key;
        }
    }

    return _key;
}

vector<uint8_t> LZW::_vec32ToVec8(const vector<pair<uint32_t, uint8_t>> &input) {
    vector<uint8_t> result;

//    cout << "input.size() = " << input.size() << endl;

    uint8_t usedBits = 0;  // число использованных битов
    uint8_t currentByte = 0; // текущий заполняемый байт

    for (const auto &x: input) {
        uint32_t code = x.first;
        int8_t bitsToWrite = x.second; // число битов, которые необходимо записать в байт

//        std::cout << "code: " << code << std::endl;
//        std::cout << "bitsToWrite: " << static_cast<int>(bitsToWrite) << std::endl;

        while (bitsToWrite > 0) {
            uint8_t canWriteToByte = 8 - usedBits;
            currentByte |= code << usedBits;
            usedBits = bitsToWrite > canWriteToByte ? 0 : bitsToWrite + usedBits;
            code >>= canWriteToByte;

            if (usedBits == 0) {
                result.push_back(currentByte);
//                cout << "currentByte: " << endl;
                currentByte = 0;
            }

            bitsToWrite -= canWriteToByte;
        }
    }

    if (usedBits != 0) {
        result.push_back(currentByte);
//        cout << "currentByte: " << endl;
    }

    if (result.size() < input.size()) {
        while (result.size() != input.size()) result.push_back(0);
    }

//    cout << "result.size() = " << result.size() << endl;

    for (auto [code, _]: input) this->codes.push_back(code);

    // Открываем файл для записи в бинарном режиме
    std::ofstream outfile("output.bin", std::ios::binary);
    if (!outfile) {
        std::cerr << "Не удалось открыть файл для записи!" << std::endl;
        return {};
    }

    // Записываем данные из вектора в файл
    outfile.write(reinterpret_cast<const char *>(this->codes.data()), this->codes.size() * sizeof(uint32_t));

    // Закрываем файл
    outfile.close();

    return result;
}

uint8_t LZW::_getBitsToRepresentInteger(uint32_t x) {
    return std::numeric_limits<uint32_t>::digits - std::countl_zero(x);
}

uint32_t LZW::_readCode(const vector<uint8_t> &inputFile, int &bytesRead, uint8_t &bitsRead, uint8_t bitsToRead) {
    uint32_t code = 0;
    uint8_t bitsReadTotal = 0;

    while (bitsToRead > 0) {
        uint8_t currentByte = inputFile[bytesRead];
        uint8_t bitsCanReadFromCurrentByte = 8 - bitsRead;
        uint8_t bitsNeedToRead = std::min(bitsToRead, bitsCanReadFromCurrentByte);
        uint8_t bitsDontNeedToRead = 8 - bitsNeedToRead - bitsRead;
        uint8_t strippedDontNeedBits = currentByte << bitsDontNeedToRead;
        uint8_t newCodePart = (strippedDontNeedBits) >> (bitsDontNeedToRead + bitsRead);

        code |= ((uint32_t) newCodePart) << bitsReadTotal;

        bitsReadTotal += bitsNeedToRead;
        bitsRead = (8 - bitsDontNeedToRead) % 8;

        bitsToRead -= std::min(bitsCanReadFromCurrentByte, bitsToRead);

        if (bitsDontNeedToRead == 0) {
            bytesRead++;
        }
    }

//    cout << "code: " << code << endl;

    return code;
}

