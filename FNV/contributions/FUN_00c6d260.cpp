struct FUN_00aa4060_class {
    void __thiscall FUN_00aa4060(void* p);
};

extern FUN_00aa4060_class DAT_011f6238;

struct FUN_00c6d260_class {
    void __thiscall FUN_00cbe880();
    FUN_00c6d260_class* __thiscall FUN_00c6d260(unsigned int flags);
};

FUN_00c6d260_class* __thiscall FUN_00c6d260_class::FUN_00c6d260(unsigned int flags)
{
    FUN_00cbe880();
    if ((flags & 1) && this) {
        DAT_011f6238.FUN_00aa4060((char*)this - ((unsigned char*)this)[-1]);
    }
    return this;
}
