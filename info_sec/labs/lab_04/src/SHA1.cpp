//
// Created by nikitalystsev on 07.12.2024.
//

#include <fstream>
#include <iostream>
#include <filesystem>
#include "SHA1.h"


mpz_class SHA1::hashFile(const string &filename) {
    vector<uint8_t> data = SHA1::_getUint8BytesFromFile(filename);

    cout << "data.size() = " << data.size() << endl;

    mpz_class result = SHA1::_hash(data);

//    cout << "result: " << result.get_str(16) << endl;

    return result;
}

mpz_class SHA1::hashText(const string &text) {
    vector<uint8_t> vUint8Str(text.begin(), text.end());

    cout << "text.size() = " << vUint8Str.size() << endl;

    mpz_class result = SHA1::_hash(vUint8Str);

    return result;
}


mpz_class SHA1::_hash(vector<uint8_t> &data) {
    uint32_t h0 = 0x67452301;
    uint32_t h1 = 0xEFCDAB89;
    uint32_t h2 = 0x98BADCFE;
    uint32_t h3 = 0x10325476;
    uint32_t h4 = 0xC3D2E1F0;

    SHA1::_preprocessing(data);

    array<uint32_t, 80> words = {0}; // 80 32-битных слов (сразу)

    for (int i = 0; i < data.size(); i += 64) {
        vector<uint8_t> chunk = SHA1::_getSlice(data, i, i + 64);

        for (uint8_t wid = 0; wid < 16; ++wid) { // заполняем первые 16 32-битных слов
            words[wid] = 0;

            for (uint8_t cid = 0; cid < 4; cid++) {
                words[wid] = (words[wid] << 8) + chunk[wid * 4 + cid];
            }
        }

        for (uint8_t j = 16; j < 80; ++j) { // 16 слов по 32-бита дополняются до 80 32-битовых слов
            words[j] = SHA1::_cyclicShiftLeft(words[j - 3] ^ words[j - 8] ^ words[j - 14] ^ words[j - 16], 1);
        }

        // инициализация хеш-значений этой части:
        uint32_t a = h0, b = h1, c = h2, d = h3, e = h4;

        // основной цикл
        for (uint8_t ind = 0; ind < 80; ++ind) {
            uint32_t f = 0, k = 0;

            if (ind < 20) {
                f = (b & c) | ((~b) & d);
                k = 0x5A827999;
            } else if (ind < 40) {
                f = b ^ c ^ d;
                k = 0x6ED9EBA1;
            } else if (ind < 60) {
                f = (b & c) | (b & d) | (c & d);
                k = 0x8F1BBCDC;
            } else {
                f = b ^ c ^ d;
                k = 0xCA62C1D6;
            }

            uint32_t temp = SHA1::_cyclicShiftLeft(a, 5) + f + e + k + words[i];
            e = d;
            d = c;
            c = SHA1::_cyclicShiftLeft(b, 30);
            b = a;
            a = temp;
        }

        // добавляем хеш-значение этой части к результату:
        h0 = h0 + a;
        h1 = h1 + b;
        h2 = h2 + c;
        h3 = h3 + d;
        h4 = h4 + e;
    }

    string resultStr = mpz_class(h0).get_str(16) +
                       mpz_class(h1).get_str(16) +
                       mpz_class(h2).get_str(16) +
                       mpz_class(h3).get_str(16) +
                       mpz_class(h4).get_str(16);

//    cout << "resultStr: " << resultStr << endl;
//    cout << "resultStr.length() = " << resultStr.length() << endl;


    return mpz_class(resultStr, 16);
}

vector<uint8_t> SHA1::_getUint8BytesFromFile(const string &filepath) {
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

void SHA1::_preprocessing(vector<uint8_t> &data) {
    uint64_t len = data.size() * 8; // длина исходного сообщения в битах

    // присоединяем бит '1' к сообщению
    data.push_back((uint8_t) 0x80);
    // 64 байта есть 512 бит, 56 байт есть 448 бит
    while (data.size() % 64 != 56) {
        data.push_back(0);
    }

    auto len_ptr = reinterpret_cast<uint8_t *>(&len);

    // добавляем в конец 64-битное представление длины до расширения
    for (int i = 0; i < 8; ++i) {
        data.push_back(*len_ptr);
        ++len_ptr;
    }
}

uint32_t SHA1::_cyclicShiftLeft(uint32_t n, uint32_t b) {
    return ((n << b) | (n >> (32 - b))) & 0xffffffff;
}

vector<uint8_t> SHA1::_getSlice(const vector<uint8_t> &v, int left, int right) {
    vector<uint8_t> res;
    res.reserve(right - left);

    for (int i = left; i < right; ++i) {
        res.push_back(v[i]);
    }

    return res;
}
