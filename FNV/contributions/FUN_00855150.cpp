struct FUN_00855130_This { TESObjectREFR* FUN_00855130(TESForm*); };
struct Chg00855220 { void* FUN_00854fe0(unsigned int); };
struct FUN_00855150_cls
{
    void FUN_00405430(unsigned int id);
    bool FUN_00855150(TESForm* form, unsigned int flags);
};

struct GlobalObj0047c850
{
    bool FUN_0047c850();
};
extern GlobalObj0047c850* DAT_011de45c;

struct RefCalls00855150
{
    void FUN_00854e70(unsigned int flags);
    int FUN_00559450();
};

struct FormCalls00855150
{
    unsigned int FUN_0084e3a0();
};

bool FUN_00855150_cls::FUN_00855150(TESForm* form, unsigned int flags)
{
    if (DAT_011de45c->FUN_0047c850())
    {
        return false;
    }
    TESObjectREFR* ref = ((FUN_00855130_This*)this)->FUN_00855130(form);
    if (ref != 0)
    {
        ((RefCalls00855150*)ref)->FUN_00854e70(flags);
        if (((RefCalls00855150*)ref)->FUN_00559450() == 0)
        {
            this->FUN_00405430(((FormCalls00855150*)form)->FUN_0084e3a0());
            TESObjectREFR* a4 = ref;
            TESObjectREFR* b = a4;
            (void)(b ? ((Chg00855220*)b)->FUN_00854fe0(1) : (void*)0);
        }
        return true;
    }
    return false;
}
