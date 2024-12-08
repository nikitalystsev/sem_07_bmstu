//
// Created by nikitalystsev on 06.12.2024.
//

#include <iostream>

#include <gmpxx.h>
#include "SHA1.h"

/*
 * Реализовать программу создания и проверки электронной подписи для документа
 * с использованием алгоритма RSA и алгоритмов хеширования MD5/SHA1 (по варианту).
 * Предусмотреть работу программы с пустым, однобайтовым файлом.
 * Программа также должна уметь обрабатывать файл архива (rar, zip или др.).
 * Вариант 2 - SHA1
 */

int main() {
    string inputFile = "../data/test.txt";
    mpz_class hashFile = SHA1::hashFile(inputFile);

    cout << "file Hash:    " << hashFile.get_str(16) << endl;

    string message = "test message";
    mpz_class hashMessage = SHA1::hashText(message);

    cout << "message Hash: " << hashMessage.get_str(16) << endl;

    return 0;
}