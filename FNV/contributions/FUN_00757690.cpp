
struct CStringArg_757690 {
    unsigned data;
    unsigned length;
    ~CStringArg_757690();
    unsigned __thiscall FUN_004048e0();
    int __thiscall FUN_00559450();
    int __thiscall FUN_00559450(int);
};
struct CValueArg_757690 {
    unsigned value;
    unsigned kind;
    unsigned other;
    ~CValueArg_757690();
    int __thiscall FUN_00ad8b30();
};
struct CWheelItem_757690 {
    void __thiscall FUN_00a01350(int id, int value);
};
struct CRelatedActor_757690 {
    bool __thiscall FUN_008c1bc0();
};
struct CInterface_757690 {
    unsigned char* __thiscall FUN_00408d60();
};
struct CRandom_757690 {
    float* __thiscall FUN_00403e20();
};
extern CInterface_757690 DAT_011d8928;
extern CRandom_757690 DAT_011d2178;
extern double DAT_01012060;
extern double DAT_01017b70;
unsigned __cdecl FUN_00ec6130(int);
unsigned __cdecl FUN_00457fe0();
struct CWheelMenu_757690 {
    void __thiscall FUN_00757690(CStringArg_757690 text, CValueArg_757690 value);
};
void __thiscall CWheelMenu_757690::FUN_00757690(CStringArg_757690 text, CValueArg_757690 value)
{
    float shift = 0.0f;
    if (text.FUN_004048e0() > 0) {
        if (*DAT_011d8928.FUN_00408d60() ||
            (*(CRelatedActor_757690**)((char*)this + 0x68) != 0 &&
             (*(CRelatedActor_757690**)((char*)this + 0x68))->FUN_008c1bc0())) {
            if (*(CWheelItem_757690**)((char*)this + 0x58)) {
                (*(CWheelItem_757690**)((char*)this + 0x58))->FUN_00a01350(0xfc4, text.FUN_00559450(1));
            }
            shift = (float)value.FUN_00ad8b30();
            if (shift == DAT_01012060) {
                shift = (float)((double)FUN_00ec6130(text.FUN_00559450()) * (*DAT_011d2178.FUN_00403e20()) * DAT_01017b70);
            }
            *(unsigned*)((char*)this + 0x78) = (unsigned)((double)FUN_00457fe0() + shift);
        }
    }
}
