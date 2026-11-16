struct FNVCallbackOwner {
    int unknown00;
    int total04;
    int unknown08;
    int (__cdecl *callback0c)(FNVCallbackOwner*, unsigned char*, int, int*, int);
};
struct FNVParameter {
    FNVCallbackOwner* owner() const {
        return *reinterpret_cast<FNVCallbackOwner* const*>(
            reinterpret_cast<const char*>(this) + 0x250);
    }
};
struct FNVChild {
    void __thiscall FUN_00a69780(FNVParameter*);
};
struct FNVMain {
    int unknown00,unknown04,unknown08,unknown0c;
    int unknown10,unknown14,unknown18,unknown1c;
    int unknown20,unknown24,unknown28,unknown2c;
    unsigned char enabled30;
    unsigned char state31, state32, state33;
    FNVChild child34;
    void __thiscall FUN_00c321f0(FNVParameter*);
    void __thiscall FUN_00c2ce70(FNVParameter*);
};
void __thiscall FNVMain::FUN_00c2ce70(FNVParameter* argument) {
    FUN_00c321f0(argument);
    unsigned char enabled = enabled30;
    FNVCallbackOwner* owner = argument->owner();
    int (__cdecl *fn)(FNVCallbackOwner*, unsigned char*, int, int*, int) = owner->callback0c;
    int value = 1;
    owner->total04 += fn(owner, &enabled, 1, &value, 1);
    child34.FUN_00a69780(argument);
}