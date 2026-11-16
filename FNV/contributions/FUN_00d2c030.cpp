struct SlowPath {
    virtual void unused0();
    virtual void unused1();
    virtual void unused2();
    virtual void unused3();
    virtual void unused4();
    virtual void unused5();
    virtual void process(int* output, int count, int value);
};
struct FUNClass {
    virtual void unused();
    virtual unsigned int generate(int value);
    SlowPath* unk04;
    void FUN_00d2c030(int* output, int count, int value);
};
void FUNClass::FUN_00d2c030(int* output, int count, int value)
{
    if (value <= 0x2000)
    {
        for (int i = 0; i < count; ++i)
            output[i] = generate(value);
        return;
    }
    unk04->process(output, count, value);
}
