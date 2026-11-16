
extern "C" unsigned char DAT_01096784;
extern "C" float DAT_01096b8c;
extern "C" unsigned int DAT_011a8400;
extern "C" unsigned int DAT_011a8404;
extern "C" unsigned int DAT_011a8408;
extern "C" unsigned int DAT_011f3704;
extern "C" unsigned int DAT_011f3708;
extern "C" unsigned int DAT_011f370c;
extern "C" unsigned int DAT_011f3710;
struct ArrayManager {
  void* FUN_00aa3e40(unsigned int size);
};
extern "C" ArrayManager DAT_011f6238;
struct FUN_00a362f0 {
  unsigned int unk00;
  unsigned int unk04;
  unsigned int unk08;
  unsigned int unk0c;
  unsigned int unk10;
  unsigned int unk14;
  unsigned int unk18;
  unsigned int unk1c;
  unsigned int unk20;
  unsigned int unk24;
  unsigned int unk28;
  unsigned int unk2c;
  unsigned int unk30;
  unsigned int unk34;
  unsigned int unk38;
  unsigned int unk3c;
  unsigned int unk40;
  volatile unsigned int unk44;
  volatile unsigned int unk48;
  unsigned int unk4c;
  unsigned int unk50;
  unsigned int unk54;
  unsigned int unk58;
  unsigned int unk5c;
  unsigned int unk60;
  unsigned int unk64;
  __declspec(nothrow) FUN_00a362f0();
  static void* operator new[](unsigned int n) {
    return DAT_011f6238.FUN_00aa3e40(n);
  }
};
struct Base {
  void* vtable;
  unsigned int unk04;
  unsigned int unk08;
  unsigned char unk0c;
  volatile unsigned char count;
  unsigned char unk0e;
  unsigned char unk0f;
  unsigned int unk10;
  unsigned int unk14;
  unsigned int unk18;
  unsigned int unk1c;
  unsigned int unk20;
  unsigned int unk24;
  unsigned int unk28;
  unsigned int unk2c;
  void FUN_00a370b0(int, float, int);
};
struct Object : Base {
  unsigned int unk30;
  unsigned int unk34;
  unsigned int unk38;
  unsigned int unk3c;
  unsigned int unk40;
  unsigned int unk44;
  unsigned int unk48;
  volatile float unk4c;
  FUN_00a362f0* unk50;
  unsigned char unk54;
  Object* FUN_00a363b0(int a, float b, int c);
};
Object* Object::FUN_00a363b0(int a, float b, int c) {
  FUN_00a370b0(a,b,c);
  vtable = &DAT_01096784;
  unk30 = DAT_011a8400;
  unk34 = DAT_011a8404;
  unk38 = DAT_011a8408;
  unk3c = DAT_011f3704;
  unk40 = DAT_011f3708;
  unk44 = DAT_011f370c;
  unk48 = DAT_011f3710;
  unk4c = DAT_01096b8c;
  unsigned char itemCount = count;
  unk50 = 0;
  unk54 = 0;
  if (itemCount > 0) {
    FUN_00a362f0* items = new FUN_00a362f0[itemCount];
    unk50 = items;
  }
  return this;
}
