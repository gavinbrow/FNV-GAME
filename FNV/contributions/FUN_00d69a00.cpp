struct hkDisplayGeometry { ~hkDisplayGeometry(); };
struct hkProcessFactory { void* FUN_00dd9380(const char*, void*); };
extern hkProcessFactory* FUN_00dd9380;
extern void* DAT_0126901c;
void FUN_00d699c0();
void FUN_00d69a00() {
    DAT_0126901c = FUN_00dd9380->FUN_00dd9380("Constraints", (void*)&FUN_00d699c0);
}
