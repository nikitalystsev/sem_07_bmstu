//
// Created by nikitalystsev on 05.10.2024.
//

#include <iostream>
#include "DES.h"
#include "PCBC.h"

using namespace std;

/*
 * Реализовать программу шифрования симметричным алгоритмом DES с
 * применением одного из режимов шифрования (по варианту).
 * Обеспечить шифрование и расшифровку произвольного файла с
 * использованием разработанной программы. Предусмотреть работу
 * программы с пустым, однобайтовым файлом. Программа также должна
 * уметь обрабатывать файл архива (rar, zip или др.).
 *
 * Вариант 2 (PCBC)
 */


int main() {
    DES des;
    bitset<64> iv("1100101001110110111101110001110101101011001001010110001101111111");

    PCBC pcbc(des, iv);

    /*
     * текстовые сообщения
     */
//    string keyForStr = "key12345";
//    string message = "Hello";
//
//    cout << "message: " << message << endl;
//
//    string encryptMessage = pcbc.encryptString(message, keyForStr);
//
//    cout << "encryptMessage: " << encryptMessage << endl;
//
//    string decryptMessage = pcbc.decryptString(encryptMessage, keyForStr);
//
//    cout << "decryptMessage: " << decryptMessage << endl;

    /*
     * произвольные файлы
     */
    string keyForFiles = "key12345";
    string filepath = "../data/test.txt";
    string encryptFilepath = "../data/encrypt_test.txt";
    string decryptFilepath = "../data/decrypt_test.txt";

    pcbc.encryptFile(filepath, encryptFilepath, keyForFiles);
    pcbc.decryptFile(encryptFilepath, decryptFilepath, keyForFiles);
}