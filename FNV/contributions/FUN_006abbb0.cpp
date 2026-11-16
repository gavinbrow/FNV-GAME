struct FUN_006abf60 {
    virtual ~FUN_006abf60();
    FUN_006abf60();
    int unk04;
    int unk08;
    int unk0c;
};
struct FUN_00aa42e0_shell {
    void* __thiscall FUN_00aa42e0();
};
FUN_00aa42e0_shell* __cdecl FUN_00401020();
struct FUN_006abbb0 : FUN_006abf60 {
    void* unk10;
    FUN_006abbb0();
    virtual ~FUN_006abbb0();
    void __thiscall FUN_009a3d00(int, int);
};
FUN_006abbb0::FUN_006abbb0() {
    unk10 = FUN_00401020()->FUN_00aa42e0();
    FUN_009a3d00(0, 0);
}