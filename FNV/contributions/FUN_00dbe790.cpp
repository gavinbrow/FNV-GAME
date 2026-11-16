struct Obj {
    void __thiscall FUN_00d605d0(unsigned char);
    void __thiscall FUN_00dbe790(__int64);
};

void __thiscall Obj::FUN_00dbe790(__int64 value)
{
    unsigned __int64 u;

    if (value < 0) {
        __int64 t = -value;
        u = ((unsigned __int64)t << 1) | 1ULL;
    } else {
        u = (unsigned __int64)value << 1;
    }

    unsigned char byte = (unsigned char)(u & 0x7f);
    u >>= 7;

    if (u != 0) {
        do {
            this->FUN_00d605d0((unsigned char)(byte | 0x80));
            byte = (unsigned char)(u & 0x7f);
            u >>= 7;
        } while (u != 0);
    }

    this->FUN_00d605d0(byte);
}
