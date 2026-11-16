void __cdecl FUN_00839dc0(bool b);
extern float DAT_01016970;
void __cdecl FUN_00839d30() {
    if (FUN_00839da0()) {
        return;
        goto initialize;
    }
    FUN_00839dc0(true);
initialize:
    for (int i = 0; i < 20; ++i) {
        *(int*)((char*)&DAT_011dd878 + 0x188 + i * 0x24) = 0;
        *(int*)((char*)&DAT_011dd878 + 0x18c + i * 0x24) = 0;
        *(float*)((char*)&DAT_011dd878 + 0x190 + i * 0x24) = DAT_01016970;
    }
}
