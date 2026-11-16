struct Factory {
    void* FUN_00dd9380(const char*, void*);
};
extern void* DAT_01268fcc;
extern Factory* DAT_01269cd0;
extern const char DAT_010d17c4;
extern void FUN_00d63d60();
void __cdecl FUN_00d63da0()
{
    DAT_01268fcc = DAT_01269cd0->FUN_00dd9380(&DAT_010d17c4, (void*)FUN_00d63d60);
}
