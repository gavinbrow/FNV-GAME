struct PrimaryBase {
 virtual ~PrimaryBase();
 unsigned int unk04,unk08,unk0c,unk10,unk14;
};
struct SecondaryBase {
 virtual void access();
 unsigned int unk1c,unk20;
};
struct TertiaryBase { virtual void access(); };
struct FUN_004092a0: PrimaryBase, SecondaryBase, TertiaryBase {
 void FUN_00409340();
 ~FUN_004092a0();
};
FUN_004092a0::~FUN_004092a0() {
 FUN_00409340();
}