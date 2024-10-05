#include <random>
#include <string>
#include <iostream>
#include <cstdint>
#include <algorithm>

#include "enigma.h"
#include "encoder.h"

using namespace std;

/*
 * Реализовать в виде программы электронный аналог шифровальной машины «Энигма».
 * Обеспечить шифрование и расшифровку произвольного файла, а также текстового
 * сообщения с использованием разработанной программы. Мощность шифруемого
 * алфавита не должна превышать 64 символа. Предусмотреть работу программы с
 * пустым, однобайтовым файлом. Программа также должна уметь обрабатывать файл
 * архива (rar, zip или др.).
 */

int main() {
    // текстовые сообщения
    vector<uint8_t> textAlp = {
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    };
    vector<vector<uint8_t>> textRotors = {
            {0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25},
            {20, 21, 22, 23, 24, 25, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0,  1,  2,  3,  4,  5,  6,  7,  8,  9},
            {7,  6,  5,  4,  3,  2,  1,  0,  24, 23, 22, 21, 20, 25, 8,  9,  19, 18, 17, 16, 15, 14, 13, 12, 11, 10}
    };
    vector<uint8_t> textReflector = {
            25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0
    };
    vector<uint8_t> textCommutator = {
            25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0
    };

    std::mt19937 textGenerator(100);
    for (auto &rotor: textRotors) {
        std::shuffle(rotor.begin(), rotor.end(), textGenerator);
    }

    Enigma textEnigmaEncrypt(
            textAlp,
            static_cast<int>(textRotors.size())
    );

    textEnigmaEncrypt.setRotors(textRotors);
    textEnigmaEncrypt.setReflector(textReflector);
    textEnigmaEncrypt.setCommutator(textCommutator);

    Enigma textEnigmaDecrypt(
            textAlp,
            static_cast<int>(textRotors.size())
    );

    textEnigmaDecrypt.setRotors(textRotors);
    textEnigmaDecrypt.setReflector(textReflector);
    textEnigmaDecrypt.setCommutator(textCommutator);

    string message = "HELLO";
    cout << "message: " << message << endl;
    string encryptMessage = textEnigmaEncrypt.encryptString(message);
    cout << "encrypt message: " << encryptMessage << endl;

    string decryptMessage = textEnigmaDecrypt.encryptString(encryptMessage);
    cout << "decrypt message: " << decryptMessage << endl;

    // произвольные файлы
    vector<uint8_t> anyFileAlp = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
    vector<vector<uint8_t>> anyFileRotors = {
            {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0},
            {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0},
            {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    };
    vector<uint8_t> anyFileReflector = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0};
    vector<uint8_t> anyFileCommutator = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0};

    std::mt19937 anyFileGenerator(100);
    for (auto &rotor: anyFileRotors) {
        std::shuffle(rotor.begin(), rotor.end(), anyFileGenerator);
    }

    Enigma anyFileEnigmaEncrypt(
            anyFileAlp,
            static_cast<int>(anyFileRotors.size())
    );

    anyFileEnigmaEncrypt.setRotors(anyFileRotors);
    anyFileEnigmaEncrypt.setReflector(anyFileReflector);
    anyFileEnigmaEncrypt.setCommutator(anyFileCommutator);

    Enigma anyFileEnigmaDecrypt(
            anyFileAlp,
            static_cast<int>(anyFileRotors.size())
    );

    anyFileEnigmaDecrypt.setRotors(anyFileRotors);
    anyFileEnigmaDecrypt.setReflector(anyFileReflector);
    anyFileEnigmaDecrypt.setCommutator(anyFileCommutator);

    string filepath = "../data/test.txt";
    string outputFilepath = "../data/encrypt_test.txt";
    anyFileEnigmaEncrypt.encryptFile(filepath, outputFilepath);

    filepath = "../data/encrypt_test.txt";
    outputFilepath = "../data/decrypt_test.txt";
    anyFileEnigmaDecrypt.encryptFile(filepath, outputFilepath);

    return 0;
}
