struct FUN_00db0920 {
    struct Entry { unsigned char key0; unsigned char key1; unsigned short value; };
    Entry entries[8];
    unsigned char flag20;
    unsigned char count;
    unsigned char flag22;
    unsigned char* FUN_00db09b0(unsigned char* result, const unsigned char* key);
};
unsigned char* FUN_00db0920::FUN_00db09b0(unsigned char* result, const unsigned char* key) {
    for (int i = count - 1; i >= 0; --i) {
        if (entries[i].key0 == key[0] && entries[i].key1 == key[1]) {
            *result = 1;
            return result;
        }
    }
    *result = 0;
    return result;
}


