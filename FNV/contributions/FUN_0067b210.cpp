struct PairOfBytes {
    unsigned char first;
    unsigned char second;
};

extern void* UNK_010688ac;

struct ConstructorHost {
    void* vtable;
    float value04;
    unsigned int value08;
    unsigned int value0C;
    unsigned char value10;
    unsigned char value11;
    float value14;
    unsigned char value18;
    unsigned int value1C;

    void FUN_0067ad20();
    ConstructorHost* FUN_0067b210(float initial, unsigned int object,
                                   PairOfBytes flags, float scale,
                                   unsigned char enabled, unsigned int reference);
};

ConstructorHost* ConstructorHost::FUN_0067b210(
    float initial, unsigned int object, PairOfBytes flags, float scale,
    unsigned char enabled, unsigned int reference) {
    FUN_0067ad20();
    vtable = &UNK_010688ac;
    value04 = initial;
    value10 = flags.first;
    value08 = object;
    value14 = scale;
    value0C = 0;
    value11 = flags.second;
    value18 = enabled;
    value1C = reference;
    return this;
}