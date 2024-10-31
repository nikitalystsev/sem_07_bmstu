//
// Created by nikitalystsev on 26.10.2024.
//

#include "AES.h"
#include "CFB.h"

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

/*
 *              nk      nb      nr
 * AES-128      4       4       10
 * AES-192      6       4       12
 * AES-256      8       4       14
 */
int main() {
    AES aes(8, 4, 14);
    vector<uint8_t> iv = {16, 15, 14, 13, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1};

    CFB cfb(aes, iv);

    /*
     * текстовые сообщения
     */
    string keyForStr = "asdfghjklqwertyuasdfghjklqwertyu";
    string message = "ffffffffffffffffaaaaaaaaaaaaaaaa";

    cout << "message: " << message << endl;

    string encryptMessage = cfb.encryptString(message, keyForStr);

    cout << "encryptMessage: " << encryptMessage << endl;

    string decryptMessage = cfb.decryptString(encryptMessage, keyForStr);

    cout << "decryptMessage: " << decryptMessage << endl;

    /*
     * произвольные файлы
     */
    string keyForFiles = "asdfghjklqwertyuasdfghjklqwertyu";
    string filepath = "../data/img.png";
    string encryptFilepath = "../data/encrypt_img.png";
    string decryptFilepath = "../data/decrypt_img.png";

    cfb.encryptFile(filepath, encryptFilepath, keyForFiles);
    cfb.decryptFile(encryptFilepath, decryptFilepath, keyForFiles);


    return 0;
}
