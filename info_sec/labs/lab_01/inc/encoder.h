//
// Created by nikitalystsev on 18.09.2024.
//

#ifndef LAB_01_ENCODER_H
#define LAB_01_ENCODER_H

#include <string>
#include <vector>
#include <cstdint>

using namespace std;

class Encoder {
private:
    vector<uint8_t> alphabet;
    size_t sizeAlph;
public:
    explicit Encoder(const vector<uint8_t> &alph);

    uint8_t encode(uint8_t symb, bool &isEncode);

    uint8_t decode(uint8_t symb, bool &isDecode);
};

#endif //LAB_01_ENCODER_H
