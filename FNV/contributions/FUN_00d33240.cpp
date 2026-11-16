struct Target {
    virtual void vfn00();
    virtual void vfn04();
    virtual void vfn08();
    virtual void vfn0c();
    virtual void vfn10();
    virtual void vfn14();
    virtual void vfn18(int a);
};

struct Self {
    int unk00;
    int unk04;
    int unk08;
    Target* unk0c;
};

void __fastcall FUN_00d33240(Self* self, int unused, int arg)
{
    self->unk0c->vfn18(arg);
}
