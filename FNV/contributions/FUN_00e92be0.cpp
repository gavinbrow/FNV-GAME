#include <windows.h>
struct S_00e92be0_Callee {
    void* __thiscall FUN_00e6e630(void* key, void** outA, void** outB);
};

struct S_00e92be0_Ref {
    virtual void f0();
    virtual void f1();
    int unk04;
};

struct S_00e92be0_Factory {
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
    S_00e92be0_Callee* unk30;

    S_00e92be0_Ref* FUN_00e92be0();
};


void S_00e92be0_Ref::f0()
{
}

void S_00e92be0_Ref::f1()
{
}

S_00e92be0_Ref* S_00e92be0_Factory::FUN_00e92be0()
{
    S_00e92be0_Callee* callee = unk30;
    if (callee != 0 && unk2c != 0) {
        void* local0 = 0;
        void* local4;

        callee->FUN_00e6e630(&unk2c, &local4, &local0);
        S_00e92be0_Ref* object =
            reinterpret_cast<S_00e92be0_Ref*>(*static_cast<void* volatile*>(&local0));

        if (object != 0) {
            if (InterlockedDecrement(reinterpret_cast<long volatile*>(&object->unk04)) == 0) {
                object->f1();
            }
        }
        return object;
    }
    return 0;
}
