extern void* DAT_010eb98c;
union ReleaseFlags { int releaseHandle; int releaseOwner; };
struct LinkOwner { void* unk00; void* unk04; void* unk08; void __thiscall FUN_00d21ce0(void*); };
struct FUN_00e3b060_Class { void* vtable; int unk04; int unk08; LinkOwner links; FUN_00e3b060_Class* __thiscall FUN_00e3b060(ReleaseFlags flags); };
FUN_00e3b060_Class* FUN_00e3b060_Class::FUN_00e3b060(ReleaseFlags flags) {
    vtable = &DAT_010eb98c;
    LinkOwner* owner = &links;
    if (flags.releaseHandle) owner->FUN_00d21ce0(owner->unk08);
    if (flags.releaseOwner) owner->FUN_00d21ce0(this);
    return this;
}