struct FUN_00dd9380_class {
    void* FUN_00dd9380(const char*, void*);
};
struct hkProcessFactory : FUN_00dd9380_class {};
struct GlobalObjectO2_00d472a0 {};
extern hkProcessFactory* FUN_00dd9380;
extern GlobalObjectO2_00d472a0 g_01268f2c;
extern void* __cdecl FUN_00d65910(void*);

void FUN_00d65950() {
    void* process = FUN_00dd9380->FUN_00dd9380("Shapes", (void*)&FUN_00d65910);
    *(void**)((char*)&g_01268f2c + 0xB4) = process;
}
