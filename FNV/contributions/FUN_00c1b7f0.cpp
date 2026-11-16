struct Object {
    Object* __thiscall FUN_00c1b5c0();
};
void* __cdecl FUN_00aa13e0(unsigned int);
Object* __cdecl FUN_00c1b7f0() {
    Object* p = (Object*)FUN_00aa13e0(0x110);
    if (p)
        return p->FUN_00c1b5c0();
    return 0;
}

