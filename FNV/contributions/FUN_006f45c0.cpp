struct FUN_006f4880 {
    int baseVptr;
    FUN_006f4880();
    ~FUN_006f4880();
};
struct FUN_006f45c0 : FUN_006f4880 {
    int unk04;
    int unk08;
    int unk0c;
    int value10;
    FUN_006f45c0();
};
extern int str_0106d91c;
struct Helper_00401020 {
    int FUN_00aa42e0();
};
extern "C" Helper_00401020* __cdecl FUN_00401020();
FUN_006f45c0::FUN_006f45c0() : FUN_006f4880() {
    baseVptr = (int)&str_0106d91c;
    value10 = FUN_00401020()->FUN_00aa42e0();
    reinterpret_cast<AX*>(this)->FUN_006b3eb0(0, 0);
}