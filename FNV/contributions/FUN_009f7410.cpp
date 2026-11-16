
struct ActorObject {
  virtual void slot00();
  virtual void slot01();
  virtual void slot02();
  virtual void slot03();
  virtual void slot04();
  virtual void slot05();
  virtual void slot06();
  virtual void slot07();
  virtual void slot08();
  virtual void slot09();
  virtual void slot10();
  virtual void slot11();
  virtual void slot12();
  virtual void slot13();
  virtual void slot14();
  virtual void slot15();
  virtual void slot16();
  virtual void slot17();
  virtual void slot18();
  virtual void slot19();
  virtual void slot20();
  virtual void slot21();
  virtual void slot22();
  virtual void slot23();
  virtual void slot24();
  virtual void slot25();
  virtual void slot26();
  virtual void slot27();
  virtual void slot28();
  virtual void slot29();
  virtual void slot30();
  virtual void slot31();
  virtual void slot32();
  virtual void slot33();
  virtual void slot34();
  virtual void slot35();
  virtual void slot36();
  virtual void slot37();
  virtual void slot38();
  virtual void slot39();
  virtual void slot40();
  virtual void slot41();
  virtual void slot42();
  virtual void slot43();
  virtual void slot44();
  virtual void slot45();
  virtual void slot46();
  virtual void slot47();
  virtual void slot48();
  virtual void slot49();
  virtual void slot50();
  virtual void slot51();
  virtual void slot52();
  virtual void slot53();
  virtual void slot54();
  virtual void slot55();
  virtual void slot56();
  virtual void slot57();
  virtual void RemoveReference(void* referencedObject);
};
struct ObjectRef {
  ActorObject* FUN_009611e0();
};
struct FUN_006708b0 {
  virtual ~FUN_006708b0();
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
  unsigned int unk44;
  unsigned int unk48;
  unsigned int unk4c;
  unsigned int unk50;
  unsigned int unk54;
  unsigned int unk58;
  unsigned int unk5c;
  unsigned int unk60;
  unsigned int unk64;
  unsigned int unk68;
  unsigned int unk6c;
  unsigned int unk70;
  unsigned int unk74;
  unsigned int unk78;
  unsigned int unk7c;
  unsigned int unk80;
  unsigned int unk84;
  unsigned int unk88;
  unsigned int unk8c;
  unsigned int unk90;
  unsigned int unk94;
  unsigned int unk98;
  unsigned int unk9c;
};
struct FUN_009f8b10 {
  unsigned int unk00;
  unsigned int unk04;
  unsigned int unk08;
  unsigned int unk0c;
  ~FUN_009f8b10();
};
struct FUN_0045cec0 {
  ObjectRef* FUN_00559450();
  void FUN_0066b0d0(int release);
  ~FUN_0045cec0();
};
struct FUN_009f7410 : FUN_006708b0 {
  FUN_009f8b10 memberA0;
  FUN_0045cec0 memberB0;
  virtual ~FUN_009f7410();
};
FUN_009f7410::~FUN_009f7410() {
  if (memberB0.FUN_00559450()) {
    if (memberB0.FUN_00559450()->FUN_009611e0()) {
      memberB0.FUN_00559450()->FUN_009611e0()->RemoveReference(memberB0.FUN_00559450());
    }
    memberB0.FUN_0066b0d0(0);
  }
}
