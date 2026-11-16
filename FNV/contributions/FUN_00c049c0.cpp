
extern float DAT_01016248;
extern void* DAT_010bcaac;

struct FUN_00ba4080_class {
    void FUN_00ba4080();
    FUN_00ba4080_class() { FUN_00ba4080(); }
    ~FUN_00ba4080_class();
};
struct FUN_00a90180_class {
    unsigned int unk28, unk2c, unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44, unk48, unk4c, unk50, unk54;
    void FUN_00a90180(unsigned int);
};
struct FourFloats {
    float x, y, z, w;
    FourFloats() : x(0.0f), y(0.0f), z(0.0f), w(0.0f) {}
    FourFloats(float a, float b, float c, float d) : x(a), y(b), z(c), w(d) {}
};
struct TailC049C0 {
    unsigned int flags;
    TailC049C0() : flags(0) {}
    ~TailC049C0();
};
struct FUN_00c049c0 : FUN_00ba4080_class {
    void* vtable;
    unsigned int unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24;
    FUN_00a90180_class region;
    FourFloats color;
    unsigned char m68, m69, m6a, m6b;
    unsigned int m6c, m70;
    TailC049C0 m74;
    FUN_00c049c0();
};
FUN_00c049c0::FUN_00c049c0()
    : vtable(&DAT_010bcaac), color(),
      m68(0), m69(0), m6a(0), m6c(0), m70(0), m74()
{
    region.FUN_00a90180(3);
    color = FourFloats(0.0f, DAT_01016248, 0.0f, 0.0f);
}
