extern "C" void __cdecl FUN_00da35f0(void*, float, float, int);
struct Owner {
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    void FUN_00d36870(float a1, float a2, int a3);
};
void Owner::FUN_00d36870(float a1, float a2, int a3) {
    FUN_00da35f0((char*)this + 0x10, a1, a2, a3);
}
