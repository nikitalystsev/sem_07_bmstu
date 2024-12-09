//
// Created by nikitalystsev on 07.12.2024.
//

#include <iostream>
#include "RSA.h"

pair<mpz_class, mpz_class> RSA::_getRandomPrimePQ(const mpz_class &minVal, const mpz_class &maxVal) {
    mpz_class p(100), q(100);

    while (p == q) {
        p = RSA::_genRandomPrime(minVal, maxVal);
        q = RSA::_genRandomPrime(minVal, maxVal);
    }

    return {p, q};
}

mpz_class RSA::_genRandomPrime(const mpz_class &minVal, const mpz_class &maxVal) {
    gmp_randclass r1(gmp_randinit_default);
    r1.seed(time(nullptr));

    mpz_class result;
    int isPrime;

    while (true) {
        result = minVal + r1.get_z_range(maxVal) % (maxVal - minVal + 1); // [minVal, maxVal]
        isPrime = mpz_probab_prime_p(result.get_mpz_t(), 10);

        if (isPrime) {
            break;
        }
    }

//    cout << "random prime number: " << result << endl;
//    cout << "random number is prime: " << isPrime << endl;

    return result;
}

mpz_class RSA::_genRandomNumber(const mpz_class &minVal, const mpz_class &maxVal) {
    gmp_randclass r1(gmp_randinit_default);
    r1.seed(time(nullptr));

    mpz_class result = minVal + r1.get_z_range(maxVal) % (maxVal - minVal + 1); // [minVal, maxVal]

//    cout << "random number: " << result << endl;

    return result;
}

pair<PrivateKey, PublicKey> RSA::genPublicAndSecretKeys() {
    mpz_class minVal(1), maxVal(string(40, '9'));

    auto [p, q] = RSA::_getRandomPrimePQ(minVal, maxVal);

//    cout << "p: " << p << endl;
//    cout << "q: " << q << endl;

    mpz_class n = p * q;
    mpz_class euler = (p - 1) * (q - 1);

//    cout << "n: " << n << endl;
//    cout << "euler: " << euler << endl;

    mpz_class e;

    while (true) {
        e = RSA::_genRandomNumber(1, euler);

        mpz_class resultGcd;
        mpz_gcd(resultGcd.get_mpz_t(), e.get_mpz_t(), euler.get_mpz_t());

        if (resultGcd == 1) {
            break;
        }
    }

//    cout << "e: " << e << endl;

    mpz_class g, s, t;

    mpz_gcdext(g.get_mpz_t(), s.get_mpz_t(), t.get_mpz_t(), e.get_mpz_t(), euler.get_mpz_t());

    mpz_class d(s);

//    cout << "d: " << d << endl;

    PublicKey publicKey{.e = e, .n = n};
    PrivateKey privateKey{.d = d, .n = n};

//    cout << "s * e % euler = " << (s * e) % euler << endl;
//    cout << "t * e % euler = " << (t * e) % euler << endl;
//    cout << "1 % euler = " << 1 % euler << endl;

    return {privateKey, publicKey};
}

mpz_class RSA::calcSignature(const mpz_class &d, const mpz_class &n, const mpz_class &hash) {
    mpz_class result;

    mpz_powm(result.get_mpz_t(), hash.get_mpz_t(), d.get_mpz_t(), n.get_mpz_t());

    return result;
}

mpz_class RSA::calcPrototypeSignature(const mpz_class &e, const mpz_class &n, const mpz_class &signature) {
    mpz_class result;

    mpz_powm(result.get_mpz_t(), signature.get_mpz_t(), e.get_mpz_t(), n.get_mpz_t());

    return result;
}

bool RSA::isCorrectSignature(const mpz_class &originalHash, const mpz_class &newHash) {
    if (originalHash != newHash) {
        return false;
    }

    return true;
}




