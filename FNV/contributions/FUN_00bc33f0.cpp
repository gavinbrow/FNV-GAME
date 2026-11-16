extern void* __cdecl FUN_00aa13e0(unsigned int size);
extern void __fastcall FUN_00a57640(void* self);
extern void* DAT_010ba948;

void* __cdecl operator new(unsigned int size) {
    return FUN_00aa13e0(size);
}

struct Base_00a57640 {
    void* m_pvt;
};

struct Derived_00bc33f0 : Base_00a57640 {
    char pad04[0x34];

    Derived_00bc33f0() {
        FUN_00a57640(this);
        m_pvt = (void*)&DAT_010ba948;
    }
};

Derived_00bc33f0* __cdecl FUN_00bc33f0() {
    return new Derived_00bc33f0();
}
