extern int DAT_0106cc78;
void* __cdecl FUN_00401020();
struct FUN_00aa42e0_Obj {
    int __thiscall FUN_00aa42e0();
};
struct FUN_006dc370 {
    void* m_vtbl;
    FUN_006dc370();
    ~FUN_006dc370();
};
struct FUN_006db890 : FUN_006dc370 {
    int unk04;
    int unk08;
    int unk0c;
    int m_value;
    FUN_006db890(int arg8, int argC, int arg10);
    void __thiscall FUN_006dc440(int first, int second);
};
FUN_006db890::FUN_006db890(int arg8, int argC, int arg10) {
    m_vtbl = &DAT_0106cc78;
    m_value = arg10 ? arg10 : ((FUN_00aa42e0_Obj*)FUN_00401020())->FUN_00aa42e0();
    FUN_006dc440(arg8, argC);
}