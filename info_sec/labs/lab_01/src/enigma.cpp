//
// Created by nikitalystsev on 18.09.2024.
//
#include <iostream>
#include <fstream>
#include <cstdint>

#include <filesystem>

#include "enigma.h"

using namespace std;

Enigma::Enigma(const vector<uint8_t> &alph, int numRotors) :
        sizeRotor{static_cast<int>(alph.size())},
        numRotors{numRotors},
        encoder(alph) {
    this->reflector = vector<uint8_t>(this->sizeRotor);
    this->commutator = vector<uint8_t>(this->sizeRotor);

    for (int i = 0; i < numRotors; i++) {
        this->rotors.emplace_back(this->sizeRotor);
    }
}

void Enigma::setReflector(vector<uint8_t> &newReflector) {
    this->reflector = newReflector;
}

void Enigma::setRotors(vector<vector<uint8_t>> &newRotors) {
    for (int i = 0; i < this->numRotors; i++)
        this->rotors[i] = newRotors[i];
}

void Enigma::setCommutator(vector<uint8_t> &newCommutator) {
    this->commutator = newCommutator;
}


uint8_t Enigma::encryptCharByCode(uint8_t code, bool &isEncrypt) {
    if (code > this->sizeRotor) {
        isEncrypt = false;
        return 0;
    }

    int encryptCode = code;

    encryptCode = this->commutator[encryptCode];

    for (int i = 0; i < this->numRotors; ++i)
        encryptCode = this->rotors[i][encryptCode];

    encryptCode = this->reflector[encryptCode];

    for (int i = this->numRotors - 1; i >= 0; --i) {
        encryptCode = this->getIndexByValueInRotor(i, encryptCode, isEncrypt);
        if (!isEncrypt) {
            return 0;
        }
    }

    int rotorQueue = 1;
    this->counter += 1;

    for (int i = 0; i < this->numRotors; ++i) {
        if (this->counter % rotorQueue == 0) {
            this->rotorRotate(i);
        }

        rotorQueue *= this->sizeRotor;
    }

    encryptCode = this->commutator[encryptCode];
    isEncrypt = true;
    return encryptCode;
}

uint8_t Enigma::getIndexByValueInRotor(int numRotor, uint8_t code, bool &isFind) {
    for (int i = 0; i < this->sizeRotor; ++i) {
        if (this->rotors[numRotor][i] == code) {
            isFind = true;
            return i;
        }
    }

    isFind = false;

    return 0;
}

void Enigma::rotorRotate(int numRotor) {
    int temp = this->rotors[numRotor][this->sizeRotor - 1];

    for (int i = this->sizeRotor - 1; i > 0; --i) {
        this->rotors[numRotor][i] = this->rotors[numRotor][i - 1];
    }

    this->rotors[numRotor][0] = temp;
}

string Enigma::encryptString(const string &str) {
    std::string encryptStr;

    for (uint8_t symbol: str) {
        bool isValid = false;

        char encryptSymbol = static_cast<char>(this->encrypt(symbol, isValid));
        if (!isValid) {
            encryptStr += static_cast<char>(symbol);
            continue;
        }

        encryptStr += static_cast<char>(encryptSymbol);
    }

    return encryptStr;
}

void Enigma::encryptFile(const string &filepath, const string &outputFilepath) {
    cout << "filesize: " << filesystem::file_size(filepath) << " bytes" << endl;

    ifstream file(filepath, ios::binary);
    if (!file.is_open()) {
        cout << "file dont open" << endl;
        return;
    }

    ofstream outputFile(outputFilepath, ios::binary);
    if (!outputFile.is_open()) {
        cout << "out file dont open" << endl;
        return;
    }

    size_t filesize = filesystem::file_size(filepath);
    size_t currByte = 0;

    while (currByte != filesize) {
        currByte++;
        char byte;
        file.read(&byte, sizeof(byte));

        unsigned char firstHalf = (byte >> 4) & 0x0F; // первые 4 бита
        unsigned char secondHalf = byte & 0x0F; // последние 4 бита

        bool isValid = false;
        char encryptFirstHalf = static_cast<char>(this->encrypt(firstHalf, isValid));
        if (!isValid) {
            outputFile.write(&byte, sizeof(byte));
            continue;
        }

        char encryptSecondHalf = static_cast<char>(this->encrypt(secondHalf, isValid));
        if (!isValid) {
            outputFile.write(&byte, sizeof(byte));
            continue;
        }

        char encryptByte = static_cast<char>((encryptFirstHalf << 4) | encryptSecondHalf);

        outputFile.write(&encryptByte, sizeof(encryptByte));
    }

    file.close();
    outputFile.close();
}

uint8_t Enigma::encrypt(uint8_t symbol, bool &isValid) {
    uint8_t symbolCode = this->encoder.encode(symbol, isValid);
    if (!isValid) {
        cout << "no encode" << endl;
        return 0;
    }
    isValid = false;
    uint8_t encryptSymbolCode = this->encryptCharByCode(symbolCode, isValid);
    if (!isValid) {
        cout << "no encrypt" << endl;
        return 0;
    }
    isValid = false;
    uint8_t encryptSymbol = this->encoder.decode(encryptSymbolCode, isValid);
    if (!isValid) {
        cout << "no decode" << endl;
        return 0;
    }

    isValid = true;
    return encryptSymbol;
}


