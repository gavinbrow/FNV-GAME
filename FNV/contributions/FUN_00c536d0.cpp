
extern "C" void __cdecl FUN_00a3da50(void*, const void*);
extern "C" void __cdecl FUN_0044adf0(void*, const void*);
struct StreamWriter {
    virtual void f00(); virtual void f04(); virtual void f08();
    virtual void f0c(); virtual void f10(); virtual void f14();
    virtual void f18(); virtual void f1c(); virtual void f20();
    virtual void f24(); virtual void f28(); virtual void f2c();
    virtual void writeObject(void*);
};
struct BoneEntryGroup {
    void** objects;
    int unk04;
    unsigned int count;
};
struct BoneLODControllerSave : NiBSBoneLODController {
    int unk08; int unk0c; int unk10; int unk14;
    int unk18; int unk1c; int unk20; int unk24;
    int unk28; int unk2c; int unk30;
    void* m_34field;
    void* m_38field;
    int unk3c;
    BoneEntryGroup** groupArray;
    unsigned short unk44;
    unsigned short groupCount;
    void __thiscall FUN_00a6d730(NiStream*);
    void __thiscall FUN_00c536d0(NiStream*);
};
void __thiscall BoneLODControllerSave::FUN_00c536d0(NiStream* stream)
{
    BoneEntryGroup* i;
    unsigned int n;
    unsigned int groupTotal;
    void* group;
    unsigned int savedCount;
    unsigned int zero;
    unsigned int object;
    unsigned int innerCount;
    unsigned int j;

    FUN_00a6d730(stream);
    FUN_00a3da50(stream, &m_34field);
    FUN_0044adf0(stream, &m_38field);
    savedCount = groupCount;
    FUN_0044adf0(stream, &savedCount);

    for (n = 0; n < groupCount; ++n) {
        i = groupArray[n];
        if (i) {
            innerCount = i->count;
            zero = innerCount;
            FUN_0044adf0(stream, &zero);
            for (groupTotal = 0; groupTotal < (j = i->count); ++groupTotal) {
                group = i->objects[groupTotal];
                reinterpret_cast<StreamWriter*>(stream)->writeObject(group);
            }
        } else {
            object = 0;
            FUN_00a3da50(stream, &object);
        }
    }
}
