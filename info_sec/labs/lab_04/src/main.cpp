//
// Created by nikitalystsev on 06.12.2024.
//

#include <iostream>

#include <gmpxx.h>
#include "SHA1.h"
#include "RSA.h"

/*
 * Реализовать программу создания и проверки электронной подписи для документа
 * с использованием алгоритма RSA и алгоритмов хеширования MD5/SHA1 (по варианту).
 * Предусмотреть работу программы с пустым, однобайтовым файлом.
 * Программа также должна уметь обрабатывать файл архива (rar, zip или др.).
 * Вариант 2 - SHA1
 */

int main() {
    auto [privateKey, publicKey] = RSA::genPublicAndSecretKeys();

    string inputFile = "../data/img.png";
    mpz_class hashFile = SHA1::hashFile(inputFile);

    cout << "hash:    " << hashFile.get_str(16) << endl;
    cout << "hash length:    " << hashFile.get_str(16).length() << endl;

    mpz_class signature = RSA::calcSignature(privateKey.d, privateKey.n, hashFile);

    cout << "signature:     " << signature.get_str(16) << endl;

    mpz_class hash = RSA::calcPrototypeSignature(publicKey.e, publicKey.n, signature);

    if (RSA::isCorrectSignature(hashFile, hash)) {
        cout << "signature is correct" << endl;
    } else {
        cout << "signature is incorrect" << endl;
    }

    return 0;
}