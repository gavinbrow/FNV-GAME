#include <string.h>
struct __declspec(align(16)) FNVState_CFA5F0 {
    int data00;
    int data04;
    int data08;
    int data0c;
    int data10;
    int data14;
    int data18;
    int data1c;
    int data20;
    int data24;
    int data28;
    int data2c;
    int data30;
    int data34;
    int data38;
    int data3c;
    int data40;
    int data44;
    int data48;
    int data4c;
    int input50;
    int input54;
    int input58;
    int input5c;
    int reserved60;
    int result64;
    float contactNormalX;
    float contactNormalY;
    float contactNormalZ;
    float contactDistance;
    void __thiscall FUN_00cfa7d0(const int* source);
};
struct FNVSIM_CFA5F0 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
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
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int* stateSource78;
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    int hasPending8c;
    int hasPending90;
    int activeCount94;
    int unk98;
    unsigned char flag9c;
    int unka0;
    int statusa4;
    void __thiscall FUN_00c91120();
    void __thiscall FUN_00c91140();
};
struct FNVAudio_CFA5F0 {
    virtual void v0();
    virtual void v1();
    virtual void v2(int id, int flags);
};
struct FNVAudioHolder_CFA5F0 {
    int unk00, unk04, unk08, unk0c;
    FNVAudio_CFA5F0* audio10;
};
extern "C" void __cdecl FUN_00cf9c60(int arg1,int arg2,FNVSIM_CFA5F0* simulation);
FNVAudioHolder_CFA5F0* __cdecl FUN_00c85750();
struct FNVOwner_CFA5F0 {
    void __thiscall FUN_00cfa400(int arg1, int arg2, FNVState_CFA5F0* state, int arg5);
    void __thiscall FUN_00cfa5f0(int arg1,int arg2,FNVSIM_CFA5F0* sim, const int* values,int arg5);
};
void __thiscall FNVOwner_CFA5F0::FUN_00cfa5f0(int arg1,int arg2,FNVSIM_CFA5F0* sim,const int* values,int arg5) {
    FNVState_CFA5F0 state;
    int* source = sim->stateSource78;
    memcpy(&state, source, 0x50);
    state.result64 = 0;
    state.FUN_00cfa7d0(source);
    state.input50 = values[0];
    state.input54 = values[1];
    state.input58 = values[2];
    state.input5c = values[3];
    ++sim->activeCount94;
    FUN_00cf9c60(arg1,arg2,sim);
    FUN_00cfa400(arg1,arg2,&state,arg5);
    if (--sim->activeCount94 == 0 && !sim->flag9c) {
        if (sim->hasPending8c) sim->FUN_00c91120();
        if (sim->statusa4 == 1 && sim->hasPending90) sim->FUN_00c91140();
    }
    if (state.result64) {
        FNVAudioHolder_CFA5F0* holder = FUN_00c85750();
        holder->audio10->v2(state.result64, 0x200);
    }
}