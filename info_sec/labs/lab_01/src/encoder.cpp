//
// Created by nikitalystsev on 18.09.2024.
//

#include "encoder.h"

#include <iostream>

using namespace std;

// Текстовый кодировщик



//Encoder::Encoder(int sizeAlph) :
//        sizeAlph{sizeAlph} {
//    for (int i = 0; i < sizeAlph; ++i) {
//        this->numAlphabet.push_back(i);
//    }
//}
//
//Encoder::Encoder(const string &alph) :
//        sizeAlph{static_cast<int>(alph.length())} {
//    this->textAlphabet = alph;
//}
//
//int Encoder::encode(int ch) {
//    for (int i = 0; i < this->sizeAlph; ++i) {
//        if (this->textAlphabet[i] == ch) {
//            return i;
//        }
//    }
//
//    return 0;
//}
//
//int Encoder::decode(int code) {
//    if (code >= this->sizeAlph) {
//        return 0;
//    }
//
//    return this->textAlphabet[code];
//}
//
//int Encoder::encodeNum(int ch, bool &isEncode) {
//    for (int i = 0; i < this->sizeAlph; ++i) {
//        if (this->numAlphabet[i] == ch) {
//            isEncode = true;
//            return i;
//        }
//    }
//
//    isEncode = false;
//
//    return 0;
//}
//
//int Encoder::decodeNum(int code) {
//    if (code >= this->sizeAlph) {
//        return 0;
//    }
//
//    return this->numAlphabet[code];
//}

Encoder::Encoder(const vector<uint8_t> &alph) :
        alphabet(alph), sizeAlph(alph.size()) {

}

uint8_t Encoder::encode(uint8_t symb, bool &isEncode) {
    for (int i = 0; i < this->sizeAlph; ++i)
        if (this->alphabet[i] == symb) {
            isEncode = true;
            return i;
        }

    isEncode = false;

    return 0;
}

uint8_t Encoder::decode(uint8_t symb, bool &isDecode) {
    if (symb >= this->sizeAlph) {
        isDecode = false;
        return symb;
    }

    isDecode = true;
    return this->alphabet[symb];
}
