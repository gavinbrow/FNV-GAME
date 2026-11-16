struct BSSpinLockUnlock { void Lock(const char*); void Unlock(); };

struct FUN_00528bb0_Class { bool FUN_00528bb0(); };

struct FUN_009062e0_Class {
    int unk00; int unk04; int unk08; int unk0C;
    int unk10; int unk14; int unk18; int unk1C;
    BSSpinLockUnlock lock;
    void* FUN_00449f80(void*);
    bool FUN_009062e0(void* a);
};

bool FUN_009062e0_Class::FUN_009062e0(void* a)
{
    lock.Lock(0);
    bool r = ((FUN_00528bb0_Class*)FUN_00449f80(a))->FUN_00528bb0();
    lock.Unlock();
    return r;
}