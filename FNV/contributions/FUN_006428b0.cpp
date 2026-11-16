struct Value_006428b0 {
 int FUN_00441110();
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
 float unk6c;
};
struct Link_006428b0 { Value_006428b0* FUN_00a59d30(); };
struct Container_006428b0 { Link_006428b0* FUN_00559450(int index); };
struct Object_006428b0 { unsigned int unk00, unk04, unk08, unk0c, unk10; Container_006428b0 unk14; float FUN_006428b0(); };
float Object_006428b0::FUN_006428b0() {
 Value_006428b0* value =
    (unk14.FUN_00559450(3)->FUN_00a59d30() == 0
      ? false
      : unk14.FUN_00559450(3)->FUN_00a59d30()->FUN_00441110() == 13)
      ? unk14.FUN_00559450(3)->FUN_00a59d30() : 0;
 if (value) return value->unk6c;
 return 0.0f;
}
