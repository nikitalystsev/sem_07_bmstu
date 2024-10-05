//
// Created by nikitalystsev on 18.09.2024.
//

#ifndef LAB_01_ENIGMA_H
#define LAB_01_ENIGMA_H

#include <vector>
#include <string>
#include "encoder.h"

using namespace std;

class Enigma {
private:
    int counter = 0; // число вращений первого ротора
    int sizeRotor; // размеры роторов (определяются мощностью алфавита)
    int numRotors; // число используемых роторов
    vector<uint8_t> reflector; // рефлектор (отражатель)
    vector<uint8_t> commutator; // коммутатор
    vector<vector<uint8_t>> rotors; // матрица роторов
    Encoder encoder; // кодировщик-декодировщик

    uint8_t getIndexByValueInRotor(int numRotor, uint8_t code, bool &isFind);

    void rotorRotate(int numRotor); // циклический сдвиг вправо

    uint8_t encrypt(uint8_t code, bool &isValid);

public:
    Enigma(const vector<uint8_t> &alph, int numRotors);

    void setReflector(vector<uint8_t> &newReflector);

    void setCommutator(vector<uint8_t> &newCommutator);

    void setRotors(vector<vector<uint8_t>> &newRotors);

    uint8_t encryptCharByCode(uint8_t code, bool &isEncrypt);

    string encryptString(const string &str);

    void encryptFile(const string &filepath, const string &outputFilepath);
};

#endif //LAB_01_ENIGMA_H
