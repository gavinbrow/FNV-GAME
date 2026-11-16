extern double _DAT_010241b0;
struct FUN_00c28490_shell {
  int unk00;
  int unk04;
  unsigned short flags;
  unsigned short unk0a;
  int unk0c;
  int unk10;
  int unk14;
  int unk18;
  int unk1c;
  int unk20;
  int unk24;
  float unk28;
  char* unk2c;
  int unk30;
  float unk34;
  char FUN_00a36250(float value);
  void FUN_00c28490(float* p);
};
void FUN_00c28490_shell::FUN_00c28490(float* p) {
  flags &= 0xfff9;
  if (unk2c != 0) {
    if (FUN_00a36250(*p) == 0) {
      if ((double)unk34 == _DAT_010241b0)
        unk34 = unk28;
      if (unk34 > unk28)
        unk2c[0xd8] = 1;
      unk34 = unk28;
    }
  }
}

