struct VtableObject { virtual void v0(); virtual void v1(int value); virtual void v2(int value); };
struct Owner {
 int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c;
 int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c;
 void FUN_00d87c20(int value, bool mode);
};
void Owner::FUN_00d87c20(int value, bool mode)
{
    VtableObject* p = (VtableObject*)((char*)this + 0x40);
    if (mode) p->v2(value); else p->v1(value);
}
