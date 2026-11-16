
struct ActiveManager {
    unsigned char __thiscall FUN_00862110();
    struct MessageInfo* __thiscall FUN_004fd3e0();
};
extern "C" ActiveManager* DAT_011de45c;
struct ParameterObject {
    int __thiscall FUN_0055b980();
    unsigned short __thiscall FUN_00497100();
};
struct StringManager {
    const unsigned char* __thiscall FUN_00408d60();
};
extern "C" StringManager DAT_011de4e8;
struct MessageInfo {
    int id;
    unsigned char kind;
};
struct MessageProvider {
    virtual void slot_000();
    virtual void slot_004();
    virtual void slot_008();
    virtual void slot_00c();
    virtual void slot_010();
    virtual void slot_014();
    virtual void slot_018();
    virtual void slot_01c();
    virtual void slot_020();
    virtual void slot_024();
    virtual void slot_028();
    virtual void slot_02c();
    virtual void slot_030();
    virtual void slot_034();
    virtual void slot_038();
    virtual void slot_03c();
    virtual void slot_040();
    virtual void slot_044();
    virtual void slot_048();
    virtual void slot_04c();
    virtual void slot_050();
    virtual void slot_054();
    virtual void slot_058();
    virtual void slot_05c();
    virtual void slot_060();
    virtual void slot_064();
    virtual void slot_068();
    virtual void slot_06c();
    virtual void slot_070();
    virtual void slot_074();
    virtual void slot_078();
    virtual void slot_07c();
    virtual void slot_080();
    virtual void slot_084();
    virtual void slot_088();
    virtual void slot_08c();
    virtual void slot_090();
    virtual void slot_094();
    virtual void slot_098();
    virtual void slot_09c();
    virtual void slot_0a0();
    virtual void slot_0a4();
    virtual void slot_0a8();
    virtual void slot_0ac();
    virtual void slot_0b0();
    virtual void slot_0b4();
    virtual void slot_0b8();
    virtual void slot_0bc();
    virtual void slot_0c0();
    virtual void slot_0c4();
    virtual void slot_0c8();
    virtual void slot_0cc();
    virtual void slot_0d0();
    virtual void slot_0d4();
    virtual void slot_0d8();
    virtual void slot_0dc();
    virtual void slot_0e0();
    virtual void slot_0e4();
    virtual void slot_0e8();
    virtual void slot_0ec();
    virtual void slot_0f0();
    virtual void slot_0f4();
    virtual void slot_0f8();
    virtual void slot_0fc();
    virtual void slot_100();
    virtual void slot_104();
    virtual void slot_108();
    virtual void slot_10c();
    virtual void slot_110();
    virtual void slot_114();
    virtual void slot_118();
    virtual void slot_11c();
    virtual void slot_120();
    virtual void slot_124();
    virtual void slot_128();
    virtual void slot_12c();
    virtual int GetDisplayValue();
};
extern "C" MessageProvider* __cdecl FUN_004839c0(int);
int __cdecl FUN_0040fbe0(const char*, ...);
extern "C" const char DAT_01012cb0[];
extern "C" const char DAT_01012c78[];
extern "C" const char DAT_0101d930[];
unsigned short __cdecl FUN_004974c0(void* unused, ParameterObject* param) {
    unsigned short count = 0;
    unsigned short initial = count;
    if (DAT_011de45c->FUN_00862110()) {
        count += 4;
        count += 2;
    }
    count += 4;
    if (param != 0 && param->FUN_0055b980()) {
        count += 2;
        count += param->FUN_00497100();
    }
    if (*DAT_011de4e8.FUN_00408d60()) {
        MessageInfo* message = DAT_011de45c->FUN_004fd3e0();
        if (message) {
            MessageProvider* provider = FUN_004839c0(message->id);
            FUN_0040fbe0(DAT_01012cb0, count - initial, message->id, provider->GetDisplayValue(), *(int*)((char*)message + 5), 0x11f3, DAT_0101d930);
        } else {
            FUN_0040fbe0(DAT_01012c78, count - initial, 0x11f3, DAT_0101d930);
        }
    }
    return count;
}
