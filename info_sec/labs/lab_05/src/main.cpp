//
// Created by nikitalystsev on 10.12.2024.
//


#include "LZW.h"

/*
 * Реализовать программу сжатия документа. Использовать алгоритм исходя из варианта.
 * Обеспечить сжатие и разжатие произвольного файла с использованием разработанной программы,
 * рассчитывать коэффициент сжатия. Предусмотреть работу программы с пустым, однобайтовым файлом.
 * Вариант 1 -- LZW
 */

int main() {
    LZW lzw;

    string inputFile = "../data/small.txt";
    string compressedFile = "../data/compressed_small.txt";
    string decompressedFile = "../data/decompressed_small.txt";

    auto [data, compressedData] = lzw.compressFile(inputFile, compressedFile);

    cout << "data.size() = " << data.size() << endl;
    cout << "compressedData.size() = " << compressedData.size() << endl;

    auto size = float(data.size()) / float(compressedData.size());
    cout << "Коэффициент сжатия : " << size << endl;

    auto [_, decompressedData] = lzw.decompressFile(compressedFile, decompressedFile);


    return 0;
}
