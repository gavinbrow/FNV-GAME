extern void* DAT_0109b220;
void* __cdecl FUN_00a5b690(unsigned int value);
struct NiFixedString {
    void* m_data;
    NiFixedString(unsigned int value) : m_data(FUN_00a5b690(value)) {}
    ~NiFixedString() {
        if (m_data != DAT_0109b220)
            InterlockedDecrement((volatile long*)((char*)m_data - 8));
    }
};
struct FUN_00c6b860_Object {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
    virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
    virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
    virtual void v20(); virtual void v21(); virtual void v22(); virtual void v23();
    virtual void v24(); virtual void v25(); virtual void v26(); virtual void v27();
    virtual void v28(); virtual void v29(); virtual void v30(); virtual void v31();
    virtual void v32(); virtual void v33(); virtual void v34(); virtual void v35();
    virtual void v36(); virtual void v37(); virtual void v38();
    virtual FUN_00c6b860_Object* Find(NiFixedString*);
    int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38;
    int unk3c; int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54;
    int unk58; int unk5c; int unk60; int unk64; int unk68; int unk6c; int unk70;
    int unk74; int unk78; int unk7c; int unk80; int unk84;
    float unk88;
};
bool __cdecl FUN_00c6b860(FUN_00c6b860_Object* object, unsigned int key) {
    bool result = false;
    if (object) {
        FUN_00c6b860_Object* selected = 0;
        if (key) {
            NiFixedString name(key);
            selected = object->Find(&name);
        }
        if (!selected)
            selected = object;
        result = selected->unk88 > 0.0f;
    }
    return result;
}