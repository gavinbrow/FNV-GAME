struct LevelValue {
    float __thiscall FUN_00a011b0(unsigned int property);
    void __thiscall FUN_00a012d0(int property, float value, int doUpdate);
    void __thiscall FUN_00700320(int property, int value);
};
struct FUN_007879f0_helper {
    unsigned int __thiscall FUN_007879f0();
};
extern const double DAT_01012060;
extern char str_0106f90c[];
extern char str_0106f8f8[];
extern "C" int __cdecl FUN_00a01860(const char*);
extern "C" float __cdecl FUN_004e4430(float);
extern "C" int __cdecl FUN_00647b70(int, int);
struct LevelMenuView {
    int unk00; int unk04; int unk08;
    LevelValue* meter0c;
    int unk10;
    LevelValue* count14;
    int unk18; int unk1c;
    float maximum20;
    void __thiscall FUN_007880a0();
};
void LevelMenuView::FUN_007880a0()
{
    if (meter0c) {
        float current = meter0c->FUN_00a011b0(0xFB0);
        int count = 1;
        if (maximum20 > DAT_01012060 && current > DAT_01012060) {
            if (maximum20 > current) {
                count = FUN_00647b70((int)FUN_004e4430(((float)(unsigned int)((FUN_007879f0_helper*)this)->FUN_007879f0() * (maximum20 - current)) / maximum20) + 1, 2);
            }
            if (count > 1) {
                meter0c->FUN_00a012d0(FUN_00a01860(str_0106f90c), (maximum20 - current) / (count - 1), 1);
            }
        }
        if (count14) {
            count14->FUN_00700320(FUN_00a01860(str_0106f8f8), count);
        }
    }
}
