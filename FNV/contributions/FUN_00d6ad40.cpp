struct FUN_00dd9380_StandIn {
    int FUN_00dd9380(const char* name, void* constructor);
};
extern FUN_00dd9380_StandIn* DAT_01269cd0;
extern int DAT_01269028;
extern char DAT_010c65b0;
void FUN_00d6ad00();
void __cdecl FUN_00d6ad40() {
    DAT_01269028 = DAT_01269cd0->FUN_00dd9380(&DAT_010c65b0, (void*)&FUN_00d6ad00);
}
