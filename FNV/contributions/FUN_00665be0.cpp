struct FUN_00665be0_interface {
    virtual void f0();
    virtual void f1();
    virtual bool f2(int, void**);
    virtual void f3();
    virtual void f4();
    virtual void f5(int);
};

struct C665be0_shell {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    void* unk10;
    void* unk14;
    void* unk18;
    FUN_00665be0_interface* unk1c;

    void FUN_00665be0(int value);
};

extern "C" void __cdecl _free(void*);

void C665be0_shell::FUN_00665be0(int value)
{
    void* result = 0;

    if (unk1c->f2(value, &result)) {
        unk1c->f5(value);

        if (result != 0) {
            _free(result);
        }
    }
}