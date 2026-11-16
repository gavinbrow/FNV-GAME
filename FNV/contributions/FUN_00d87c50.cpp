struct Primary { virtual void Operation(); unsigned int unk04; };
struct Interface0 { virtual void Operation(); };
struct Interface1 { virtual void Operation(); };
struct Interface2 { virtual void Operation(); };
struct Interface3 { virtual void Operation(); };
struct FUN_00def350 : Primary, Interface0, Interface1, Interface2, Interface3 {
 unsigned int unk18;
 unsigned int unk1C;
 unsigned int unk20;
 unsigned int unk24;
 unsigned int unk28;
 unsigned int unk2C;
 unsigned int unk30;
 unsigned int unk34;
 unsigned int unk38;
 unsigned int unk3C;
 FUN_00def350(void*);
};
struct Secondary { virtual void Operation(); Secondary() {} };
struct FUN_00d87c50 : FUN_00def350, Secondary { FUN_00d87c50(void*); virtual void AnotherOperation(); };
FUN_00d87c50::FUN_00d87c50(void* p) : FUN_00def350(p) { unk20=6; }

