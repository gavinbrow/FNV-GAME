extern "C" void* __cdecl FUN_004b7210();

struct FUN_009373f0_StandIn {
    unsigned char __thiscall FUN_009373f0();
};

struct FUN_009b7010_StandIn {
    void __thiscall FUN_009b7010(int*);
};

extern int DAT_011f426c;

struct ThreeInts {
    int a;
    int b;
    int c;
};

int* __cdecl FUN_007033d0(int* arg) {
    if (FUN_004b7210() &&
        ((FUN_009373f0_StandIn*)FUN_004b7210())->FUN_009373f0()) {
        ((FUN_009b7010_StandIn*)FUN_004b7210())->FUN_009b7010(arg);
        return arg;
    }

    *(ThreeInts*)arg = *(const ThreeInts*)&DAT_011f426c;
    return arg;
}
