//
// Created by nikitalystsev on 07.12.2024.
//

#ifndef LAB_04_SHA1_H
#define LAB_04_SHA1_H

#include <vector>
#include <cstdint>
#include <string>
#include <array>
#include <gmpxx.h>

using namespace std;

class SHA1 {
private:
    static vector<uint8_t> _getUint8BytesFromFile(const string &filepath);

    static void _preprocessing(vector<uint8_t> &data);

    static vector<uint8_t> _getSlice(const vector<uint8_t> &v, int left, int right);

    static uint32_t _cyclicShiftLeft(uint32_t n, uint32_t b);

    static mpz_class _hash(vector<uint8_t> &data);

public:
    SHA1() = default;

    ~SHA1() = default;

    static mpz_class hashFile(const string &filename);

    static mpz_class hashText(const string &text);
};


#endif //LAB_04_SHA1_H
