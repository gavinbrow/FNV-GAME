struct Callback {
    virtual void unk00();
    virtual void unk04();
    virtual void unk08();
    virtual void unk0c();
    virtual void unk10();
    virtual void unk14();
    virtual void unk18();
    virtual void* invoke(void* argument);
};
struct FUN_00dbab50_cls {
    void __thiscall FUN_00dbab50(void* value);
};
struct FUN_00dbaea0_cls {
    Callback* target;
    FUN_00dbab50_cls* __thiscall FUN_00dbaea0(FUN_00dbab50_cls* output, void* argument);
};
FUN_00dbab50_cls* __thiscall FUN_00dbaea0_cls::FUN_00dbaea0(FUN_00dbab50_cls* output, void* argument) {
    output->FUN_00dbab50(this->target->invoke(argument));
    return output;
}
