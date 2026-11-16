struct DefaultPathSource {
    void* FUN_00aa42e0();
};
DefaultPathSource* __cdecl FUN_00401020();
struct FUN_005e04c0 {
    FUN_005e04c0();
    virtual ~FUN_005e04c0();
};
struct FUN_006cf3a0 : FUN_005e04c0 {
    int unk04;
    int unk08;
    int unk0c;
    void* unk10;
    FUN_006cf3a0(int arg1, int arg2, void* source);
    virtual ~FUN_006cf3a0();
    void FUN_006b3eb0(int arg1, int arg2);
};
FUN_006cf3a0::FUN_006cf3a0(int arg1, int arg2, void* source) : FUN_005e04c0() {
    unk10 = source ? source : FUN_00401020()->FUN_00aa42e0();
    FUN_006b3eb0(arg1, arg2);
}