#include <math.h>

struct ThresholdState {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    float threshold;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int mode;
};

struct ValueSource {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
};

extern "C" float __cdecl FUN_00c74c20();
typedef float (__thiscall *ReadValue)(void*);

unsigned char __cdecl FUN_00ce57c0(ThresholdState* state, void* unused1,
                                  void* unused2, ValueSource* first,
                                  ValueSource* second) {
    if (state->mode != 1) return 1;

    float a = fabs(reinterpret_cast<ReadValue>(FUN_00c74c20)(
        reinterpret_cast<char*>(first) + 0x10));
    float b = fabs(reinterpret_cast<ReadValue>(FUN_00c74c20)(
        reinterpret_cast<char*>(second) + 0x10));
    float maximum = a > b ? a : b;
    return static_cast<unsigned char>(maximum <= state->threshold);
}
