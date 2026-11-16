struct Prefix {
    virtual void slot();
    unsigned int f04; unsigned int f08; unsigned int f0c; unsigned int f10;
    unsigned int f14; unsigned int f18; unsigned int f1c; unsigned int f20;
    unsigned int f24; unsigned int f28; unsigned int f2c; unsigned int f30;
    unsigned int f34; unsigned int f38; unsigned int f3c; unsigned int f40;
    unsigned int f44; unsigned int f48; unsigned int f4c; unsigned int f50;
    unsigned int f54;
    int __thiscall FUN_00cd2260(int value);
};
struct FUN_00cd2460_class;
struct Secondary {
    virtual int FUN_00cd2460(int value);
};
struct FUN_00cd2460_class : Prefix, Secondary {};
int __thiscall Secondary::FUN_00cd2460(int value) {
    return reinterpret_cast<Prefix*>(reinterpret_cast<char*>(this) - sizeof(Prefix))->FUN_00cd2260(value);
}

