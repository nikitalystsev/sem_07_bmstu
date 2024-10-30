//
// Created by nikitalystsev on 26.10.2024.
//

#include "AES.h"

/*
 * Реализовать программу шифрования симметричным алгоритмом AES
 * с применением одного из режимов шифрования (по варианту).
 * Обеспечить шифрование и расшифровку произвольного файла с
 * использованием разработанной программы. Предусмотреть работу программы
 * с пустым, однобайтовым файлом. Программа также должна уметь
 * обрабатывать файл архива (rar, zip или др.).
 *
 * Вариант 3 (CFB)
 */


void printBlock(const vector<uint8_t> &matrix) {
    for (const auto &val: matrix) {
        cout << static_cast<int>(val) << " ";
    }
    cout << endl;
}

int main() {
    AES aes(4, 4, 10);

    vector<uint8_t> msg = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
    vector<uint8_t> key = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};

    std::cout << "message: " << std::endl;
    printBlock(msg);

    vector<uint8_t> encryptMsg = aes.encryptBlock(msg, key);

    std::cout << "encrypt message: " << std::endl;
    printBlock(encryptMsg);

    vector<uint8_t> decryptMsg = aes.decryptBlock(encryptMsg, key);

    std::cout << "decrypt message: " << std::endl;
    printBlock(decryptMsg);


    return 0;
}
