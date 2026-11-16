struct FUN_00a1c4a0 : Menu_007a8b10 {
    FUN_00a1c4a0();
};
struct FUN_00730810 {
    FUN_00730810();
    ~FUN_00730810();
};
extern char DAT_0106ed20;
extern char DAT_0106ed18;
extern char DAT_01075da0;
extern char DAT_01075d94;
extern int DAT_011da7e0;
extern int DAT_011da7e8;
extern int DAT_011da7e4;
extern int __cdecl FUN_00a01860(const char*);
struct FUN_007b7400 : FUN_00a1c4a0 {
    FUN_00730810 inner;
    FUN_007b7400();
    virtual ~FUN_007b7400();
};
FUN_007b7400::FUN_007b7400() {
    DAT_011da7e0 = FUN_00a01860(&DAT_0106ed20);
    DAT_011da7e8 = FUN_00a01860(&DAT_0106ed18);
    DAT_011da7e4 = FUN_00a01860(&DAT_01075da0);
    DAT_011da7dc = FUN_00a01860(&DAT_01075d94);
    *((int*)((char*)this + 0x98)) = 0;
}