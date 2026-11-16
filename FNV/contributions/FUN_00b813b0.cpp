struct RTTI {
    const char* name;
    RTTI* parent;
};

extern RTTI g_rttiA;
extern RTTI g_rttiB;

struct Child {
    virtual void vfn00();
    virtual void vfn04();
    virtual RTTI* GetRTTI();
};

typedef void (__cdecl *Callback)(Child*, int, int);

struct Self {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    Child* children[2];
    void __thiscall FUN_00b813b0(Callback cb, int arg);
};

void __thiscall Self::FUN_00b813b0(Callback cb, int arg)
{
    for (int i = 0; i < 2; i++) {
        Child* c = children[i];
        if (c) {
            bool found = false;
            for (RTTI* r = c->GetRTTI(); r; r = r->parent) {
                if (r == &g_rttiA) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                Child* d = children[i];
                if (d) {
                    for (RTTI* r = d->GetRTTI(); r && r != &g_rttiB; r = r->parent) {
                    }
                }
            }
            cb(children[i], 0, arg);
        }
    }
}
