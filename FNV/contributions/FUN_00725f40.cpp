class Tile {
public:
    float GetFloat(int value);
    void Set(int value, float amount, bool mode);
    void Set(int value, int count);
};
extern double DAT_01012060;
extern float __cdecl FUN_004e4430(float value);
extern int __cdecl FUN_00647b70(int lower, int upper);
extern int __cdecl FUN_00a01860(const char* name);
struct FUN_00725f40_shell {
    int unk00;
    int unk04;
    int unk08;
    Tile* unk0c;
    int unk10;
    Tile* unk14;
    int unk18;
    int unk1c;
    float unk20;
    int FUN_00726920();
    void FUN_00725f40();
};
void FUN_00725f40_shell::FUN_00725f40()
{
    if (unk0c != 0) {
        float iStack_c = unk0c->GetFloat(0xfb0);
        {
        int fVar1 = 1;
        if (unk20 > DAT_01012060 && iStack_c > DAT_01012060) {
            if (unk20 > iStack_c) {
                fVar1 = FUN_00647b70((int)FUN_004e4430((float)(unsigned int)FUN_00726920() * (unk20 - iStack_c) / unk20) + 1, 2);
            }
            if (fVar1 > 1) {
                unk0c->Set(FUN_00a01860("_scroll_delta"), (unk20 - iStack_c) / (fVar1 - 1), true);
            }
        }
        if (unk14 != 0) {
            unk14->Set(FUN_00a01860("_number_of_items"), fVar1);
        }
        }
    }
}


