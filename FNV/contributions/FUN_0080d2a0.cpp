struct Temp
{
    void* vtable; float value; unsigned int unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24,unk28,unk2c,unk30,unk34,unk38,unk3c,unk40,unk44,unk48;
    Temp(unsigned int, unsigned int, unsigned int);
};
struct Owner
{
    unsigned int unk00,unk04,arg08,arg0c,unk10,unk14,unk18,unk1c,unk20,unk24,arg28;
    void FUN_00804090(Temp*);
    Temp* FUN_0080d2a0();
};
Temp* Owner::FUN_0080d2a0()
{
    Temp* p = new Temp(arg28, arg08, arg0c);
    FUN_00804090(p);
    return p;
}
