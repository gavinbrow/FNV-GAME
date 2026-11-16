struct TESForm {};
extern "C" char DAT_01183028, DAT_01183004;
extern "C" void* __cdecl FUN_00ec43fb(void*, int, const void*, const void*, int);
extern "C" int __cdecl FUN_00ec4835(const void*, const void*, unsigned int);
struct ScriptS { void* FUN_00500940(); };
struct ZoneBaseComparison { bool FUN_00485270(TESForm*); };
struct Test : ZoneBaseComparison { ScriptS script; bool FUN_00401480(TESForm*); };
// @fnv 0x00401480
bool Test::FUN_00401480(TESForm* target)
{
    Test* other = reinterpret_cast<Test*>(FUN_00ec43fb(target, 0, &DAT_01183028, &DAT_01183004, 0));
    if (!other)
        return true;
    if (FUN_00485270(reinterpret_cast<TESForm*>(other)))
        return true;
    if (FUN_00ec4835(script.FUN_00500940(), other->script.FUN_00500940(), 8) != 0)
        return true;
    return false;
}
