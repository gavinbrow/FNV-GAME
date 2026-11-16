extern "C" unsigned short DAT_01202e2a;

struct FUN_00c45b20_Class {
    void __thiscall FUN_00c45b20(unsigned int value);
};

extern "C" FUN_00c45b20_Class DAT_01202e20;

struct FUN_00c45ae0_LocalState {
    int field00;
    int field04;
    int field08;
    int field0C;
    int field10;
    int field14;
    int field18;
    int field1C;
    int field20;
    int field24;
    int field28;
    int field2C;
    int field30;
    int field34;
    int field38;
    int field3C;
    int field40;
    int field44;
    int field48;
    int field4C;
    int field50;
    int field54;
    int field58;
    int field5C;
    int field60;
    int field64;
};

void __cdecl FUN_00c45ae0(unsigned int value)
{
    FUN_00c45ae0_LocalState localState;

    if (DAT_01202e2a < value) {
        DAT_01202e20.FUN_00c45b20(value);
    }
}