struct Foo {
    char m0;
    void FUN_00681530(int value);
};

void Foo::FUN_00681530(int value) {
    int temp = value;
    if (value < 0 || value >= 6) {
        temp = 0;
    }
    temp <<= 5;
    m0 &= 0xffffff1f;
    m0 |= (char)temp;
}
