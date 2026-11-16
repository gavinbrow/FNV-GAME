struct TriStrips_A923B0 {
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
  unsigned short m_usActiveVertices;
  unsigned short m_usActiveTriangles;
  unsigned short FUN_00a923b0() const;
};
unsigned short TriStrips_A923B0::FUN_00a923b0() const { return m_usActiveTriangles; }