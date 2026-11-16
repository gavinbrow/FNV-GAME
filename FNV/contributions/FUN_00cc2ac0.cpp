
extern "C" unsigned char DAT_010c955c;
extern "C" int DAT_012685ac;
void __cdecl FUN_00c876a0();
struct FUN_00c8a720 {
  void* vtable;
  virtual ~FUN_00c8a720();
};
struct FUN_00cc2ac0 : FUN_00c8a720 {
  virtual ~FUN_00cc2ac0();
};
FUN_00cc2ac0::~FUN_00cc2ac0() {
  FUN_00c876a0();
  --DAT_012685ac;
}
