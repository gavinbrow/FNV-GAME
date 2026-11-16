struct NiPoint3; struct NiColorA; struct NiPoint2;
enum NiGeometryData__DataFlags { Flag0 = 0 };
struct NiTriShapeData {
    virtual void v00();
    unsigned short unk04;
    unsigned short unk06;
    unsigned short unk08;
    unsigned short unk0a;
    unsigned int unk0c; unsigned int unk10; unsigned int unk14; unsigned int unk18; unsigned int unk1c;
    unsigned int unk20; unsigned int unk24; unsigned int unk28; unsigned int unk2c;
    unsigned int unk30; unsigned int unk34; unsigned int unk38; unsigned int unk3c;
    unsigned short unk40; unsigned short unk42; unsigned int unk44;
    unsigned int unk48; unsigned int unk4c; unsigned int unk50; unsigned int unk54;
    NiTriShapeData(unsigned short, NiPoint3*, NiPoint3*, NiColorA*, NiPoint2*, unsigned short, NiGeometryData__DataFlags, unsigned short, unsigned short*);
};
struct NiTriStripsData : NiTriShapeData {
    unsigned short unk58;
    unsigned short unk5a;
    NiTriStripsData(unsigned short, NiPoint3*, NiPoint3*, NiColorA*, NiPoint2*, unsigned short, NiGeometryData__DataFlags, unsigned short, unsigned short*, unsigned short, unsigned short);
};
NiTriStripsData::NiTriStripsData(unsigned short p1, NiPoint3* p2, NiPoint3* p3, NiColorA* p4, NiPoint2* p5, unsigned short p6, NiGeometryData__DataFlags p7, unsigned short p8, unsigned short* p9, unsigned short p10, unsigned short p11)
    : NiTriShapeData(p10, p2, p3, p4, p5, p6, p7, p11, p9), unk58(p10), unk5a(p11) {
    unk08 = p1;
    unk40 = p8;
    unk44 = p8 * 3;
}

