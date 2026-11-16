struct Intf {
    virtual int unk0();
    virtual int unk1();
    virtual int unk2();
    virtual int unk3();
    virtual int unk4();
    virtual int m0();
    virtual int m1();
};

int Intf::unk0() { return 0; }
int Intf::unk1() { return 0; }
int Intf::unk2() { return 0; }
int Intf::unk3() { return 0; }
int Intf::unk4() { return 0; }
int Intf::m0() { return 0; }
int Intf::m1() { return 0; }

int __stdcall FUN_009fa0d0(int a)
{
    Intf* p = *(Intf**)(a + 0xC);
    int r = p->m0();
    p = *(Intf**)(a + 0xC);
    *(int*)(a + 0x10) = r;
    *(int*)(a + 0x08) = p->m1();
    *(int*)(a + 0x04) = 0;
    return 0;
}
