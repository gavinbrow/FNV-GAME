struct FUN_0043b4a0_Target {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual struct FUN_00a59d30_shell* FUN_Virtual0x18();
};

struct FUN_0045bc00_shell {
    int FUN_0045bc00(int);
    FUN_0043b4a0_Target* FUN_0043b4a0(int);
};

void* FUN_00438220();

struct FUN_00441130_shell {
    void FUN_00441130(int, bool);
};

struct FUN_00a59d30_shell {
    FUN_00441130_shell* FUN_00a59d30(void*);
};

struct FUN_0045c9e0_shell {
    void* unk00;
    void* unk04;
    GridCellArray* cells;
    void FUN_0045c9e0(int x, int y, bool flag);
};

void FUN_0045c9e0_shell::FUN_0045c9e0(int x, int y, bool flag)
{
    TESObjectCELL** cell = (TESObjectCELL**)cells->Get(x, y);
    if (cell && *cell) {
        int i;
        FUN_00a59d30_shell* obj;
        for (i = 0; i < 4; i++) {
            NiAVObject* node = ((FUN_0045c9a0_shell*)*cell)->FUN_0045c9a0(i);
            obj = ((FUN_0045bc00_shell*)node)->FUN_0045bc00(0) ? ((FUN_0045bc00_shell*)node)->FUN_0043b4a0(0)->FUN_Virtual0x18() : 0;
            if (obj) {
                FUN_00441130_shell* target = obj->FUN_00a59d30(FUN_00438220());
                target->FUN_00441130(0x34, !flag);
            }
        }
    }
}
