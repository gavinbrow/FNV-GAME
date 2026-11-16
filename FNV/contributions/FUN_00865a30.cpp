struct FUN_00865aa0_shell {
    unsigned char c;
    void __thiscall FUN_00865aa0(unsigned int a);
};
struct FUN_00865c80_shell {
    unsigned char c;
    void __thiscall FUN_00865c80(void* buffer, unsigned int value);
};
struct FUN_00846330_shell {
    void __thiscall FUN_00846330(void* data, int size);
};
struct _ref_0084e3a0_shell {
    unsigned int __thiscall _ref_0084e3a0();
};
unsigned int __cdecl FUN_00845d40(unsigned int);
void __cdecl FUN_00845d80(void*, unsigned int, unsigned int);
struct FUN_00865a30_owner {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    void __thiscall FUN_00865a30(void* buffer);
};
void FUN_00865a30_owner::FUN_00865a30(void* buffer) {
    unsigned int secondValue = ((_ref_0084e3a0_shell*)this)->_ref_0084e3a0();
    unsigned int firstValue = FUN_00845d40(secondValue);
    ((FUN_00865aa0_shell*)((char*)this + 0x1b))->FUN_00865aa0(firstValue);
    ((FUN_00846330_shell*)buffer)->FUN_00846330((char*)this + 0x14, 9);
    FUN_00845d80(buffer, secondValue, firstValue);
    ((FUN_00865c80_shell*)this)->FUN_00865c80(buffer, secondValue);
}

