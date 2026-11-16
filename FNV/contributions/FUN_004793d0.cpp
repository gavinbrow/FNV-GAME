extern const char DAT_01183040[];
extern const char DAT_01183290[];
extern "C" void* __cdecl FUN_00ec43fb(int, int, const char*, const char*, int);
struct LookupObject { int __thiscall FUN_00726070(); };
struct QueryObject {
    bool __thiscall FUN_004793d0(int);
    int __thiscall FUN_00726070();
};
bool __thiscall QueryObject::FUN_004793d0(int argument) {
    void* found = FUN_00ec43fb(argument, 0, DAT_01183040, DAT_01183290, 0);
    if (found == 0)
        return true;
    if (FUN_00726070() != ((LookupObject*)found)->FUN_00726070())
        return true;
    return false;
}
