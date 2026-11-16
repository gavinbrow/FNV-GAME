
extern int DAT_01015e4c;
extern "C" void __cdecl FUN_00401030(void*);

struct EmittanceSourceCleanup : BSExtraData {
    void* ownedSource;
    void __thiscall FUN_0040ecb0();
    void __thiscall FUN_004355f0();
};

void __thiscall EmittanceSourceCleanup::FUN_004355f0()
{
    *reinterpret_cast<void**>(this) = &DAT_01015e4c;
    void* sourceToFree = ownedSource;
    FUN_00401030(sourceToFree);
    FUN_0040ecb0();
}
