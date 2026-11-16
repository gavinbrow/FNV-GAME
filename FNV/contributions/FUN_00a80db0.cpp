struct ReaderStub
{
    void* m_vtable;
    unsigned int m_uiPosition;
    unsigned int unk08;
    int (__cdecl* m_pRead)(ReaderStub*, void*, unsigned int, unsigned int*, unsigned int);
    template <class T> void LoadValue(T& value)
    {
        unsigned int uiElem = sizeof(T);
        m_uiPosition += m_pRead(this, &value, sizeof(T), &uiElem, 1);
    }
};
class StreamStub
{
public:
    virtual void Slot00(); virtual void Slot04(); virtual void Slot08(); virtual void Slot0C();
    virtual void Slot10(); virtual void Slot14(); virtual void Slot18(); virtual void Slot1C();
    virtual void Slot20(); virtual void Slot24(); virtual void Slot28(); virtual void Slot2C();
    virtual void vfn_30(void* value);
int unk004; int unk008; int unk00C; int unk010; int unk014; int unk018;
    int unk01C; int unk020; int unk024; int unk028; int unk02C; int unk030;
    int unk034; int unk038; int unk03C; int unk040; int unk044; int unk048;
    int unk04C; int unk050; int unk054; int unk058; int unk05C; int unk060;
    int unk064; int unk068; int unk06C; int unk070; int unk074; int unk078;
    int unk07C; int unk080; int unk084; int unk088; int unk08C; int unk090;
    int unk094; int unk098; int unk09C; int unk0A0; int unk0A4; int unk0A8;
    int unk0AC; int unk0B0; int unk0B4; int unk0B8; int unk0BC; int unk0C0;
    int unk0C4; int unk0C8; int unk0CC; int unk0D0; int unk0D4; int unk0D8;
    int unk0DC; int unk0E0; int unk0E4; int unk0E8; int unk0EC; int unk0F0;
    int unk0F4; int unk0F8; int unk0FC; int unk100; int unk104; int unk108;
    int unk10C; int unk110; int unk114; int unk118; int unk11C; int unk120;
    int unk124; int unk128; int unk12C; int unk130; int unk134; int unk138;
    int unk13C; int unk140; int unk144; int unk148; int unk14C; int unk150;
    int unk154; int unk158; int unk15C; int unk160; int unk164; int unk168;
    int unk16C; int unk170; int unk174; int unk178; int unk17C; int unk180;
    int unk184; int unk188; int unk18C; int unk190; int unk194; int unk198;
    int unk19C; int unk1A0; int unk1A4; int unk1A8; int unk1AC; int unk1B0;
    int unk1B4; int unk1B8; int unk1BC; int unk1C0; int unk1C4; int unk1C8;
    int unk1CC; int unk1D0; int unk1D4; int unk1D8; int unk1DC; int unk1E0;
    int unk1E4; int unk1E8; int unk1EC; int unk1F0; int unk1F4; int unk1F8;
    int unk1FC; int unk200; int unk204; int unk208; int unk20C; int unk210;
    int unk214; int unk218; int unk21C; int unk220; int unk224; int unk228;
    int unk22C; int unk230; int unk234; int unk238; int unk23C; int unk240;
    int unk244; int unk248; int unk24C;
    ReaderStub* m_pkReader;
};
class GeometryStub
{
public:
    int unk000; int unk004; int unk008; int unk00C; int unk010; int unk014;
    int unk018; int unk01C; int unk020; int unk024; int unk028; int unk02C;
    int unk030; int unk034; int unk038; int unk03C; int unk040; int unk044;
    int unk048; int unk04C; int unk050; int unk054; int unk058; int unk05C;
    int unk060; int unk064; int unk068; int unk06C; int unk070; int unk074;
    int unk078; int unk07C; int unk080; int unk084; int unk088; int unk08C;
    int unk090; int unk094; int unk098; int unk09C; int unk0A0; int unk0A4;
    int unk0A8; int unk0AC; int unk0B0; int unk0B4;
    void* m_spModelData;
    void* m_spSkinInstance;
    void SaveBinary(StreamStub& stream);
    void FUN_00a80db0(StreamStub& stream);
};
template <class T> void LoadStreamValue(StreamStub& stream, T& value)
{
    ReaderStub* reader = stream.m_pkReader;
    unsigned int uiElem = sizeof(T);
    reader->m_uiPosition += reader->m_pRead(reader, &value, uiElem, &uiElem, 1);
}
void GeometryStub::FUN_00a80db0(StreamStub& stream)
{
    SaveBinary(stream);
    stream.vfn_30(m_spModelData);
    stream.vfn_30(m_spSkinInstance);
    unsigned int uiData0 = 0; stream.m_pkReader->LoadValue(uiData0);
    { unsigned int uiData1 = 0; stream.m_pkReader->LoadValue(uiData1); }
    unsigned char ucData2 = 0; stream.m_pkReader->LoadValue(ucData2);
}
