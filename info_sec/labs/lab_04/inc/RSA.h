//
// Created by nikitalystsev on 07.12.2024.
//

#ifndef LAB_04_RSA_H
#define LAB_04_RSA_H

#include <utility>
#include <cstdint>
#include <gmpxx.h>

using namespace std;

struct PublicKey {
    mpz_class e;
    mpz_class n;
};

struct PrivateKey {
    mpz_class d;
    mpz_class n;
};

class RSA {
private:
    static mpz_class _genRandomPrime(const mpz_class &minVal, const mpz_class &maxVal);

    static mpz_class _genRandomNumber(const mpz_class &minVal, const mpz_class &maxVal);

    static pair<mpz_class, mpz_class> _getRandomPrimePQ(const mpz_class &minVal, const mpz_class &maxVal);

public:
    RSA() = default;

    ~RSA() = default;

    static pair<PrivateKey, PublicKey> genPublicAndSecretKeys();

    // вычислить подпись
    static mpz_class calcSignature(const mpz_class &d, const mpz_class &n, const mpz_class &hash);

    // вычислить прообраз сообщения
    static mpz_class calcPrototypeSignature(const mpz_class &e, const mpz_class &n, const mpz_class &signature);

    static bool isCorrectSignature(const mpz_class &hash, const mpz_class &signature);
};

#endif //LAB_04_RSA_H
