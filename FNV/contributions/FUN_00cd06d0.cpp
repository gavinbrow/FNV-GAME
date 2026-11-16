struct Outer { char head[28]; };
typedef void (__thiscall *VCall)(void*);
void __fastcall FUN_00cd06d0(Outer* self) {
    void* p = (char*)self + 28;
    volatile VCall* table = *(VCall**)p;
    table[23](p);
}