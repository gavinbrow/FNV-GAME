extern "C" char DAT_010ebd64;
struct Obj {
    const void* vptr;
    Obj* FUN_00e40ca0(int unused);
};

Obj* Obj::FUN_00e40ca0(int unused) {
    vptr = &DAT_010ebd64;
    return this;
}
