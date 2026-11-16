struct NiMemObject {
    static void* __cdecl operator new(unsigned int size);
};
struct NiFloatData;
struct NiFloatInterpolator : NiMemObject {
    virtual void v00(); virtual void ReleaseWhenZero();
    virtual void v02(); virtual void v03(); virtual void v04(); virtual void v05();
    virtual void v06(); virtual void v07(); virtual void v08(); virtual void v09();
    virtual void v10(); virtual void v11(); virtual void v12(); virtual void v13();
    virtual void v14(); virtual void v15(); virtual void v16(); virtual void v17();
    virtual void v18(); virtual void v19(); virtual void v20(); virtual void v21();
    virtual void v22(); virtual void v23(); virtual void v24(); virtual void v25();
    virtual void v26(); virtual void v27(); virtual void v28(); virtual void v29();
    virtual void v30(); virtual void v31(); virtual void v32(); virtual void v33();
    virtual void v34(); virtual void v35(); virtual void v36(); virtual void v37();
    virtual void v38(); virtual void v39(); virtual void v40(); virtual void v41();
    virtual void v42(); virtual void v43(); virtual void v44(); virtual void v45();
    virtual void v46(); virtual void Finalize();
    long ref_count;
    int unk08; int unk0c; int unk10; int unk14;
    NiFloatInterpolator(NiFloatData* data);
};
struct FUN_00a63430_class { NiFloatData* FUN_00a63430(); };
struct FUN_00bc3540_class {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30;
    NiFloatInterpolator* m_object34;
    void FUN_00a57630(void* value);
    void FUN_00bc3540(void* value);
};
void FUN_00bc3540_class::FUN_00bc3540(void* value)
{
    FUN_00a57630(value);
    if (*(unsigned int*)((char*)value + 0xd8) < 0x0a010068u) {
        NiFloatData* data = ((FUN_00a63430_class*)value)->FUN_00a63430();
        NiFloatInterpolator* replacement = new NiFloatInterpolator(data);
        NiFloatInterpolator* old = m_object34;
        if (old != replacement) {
            if (old != 0 && InterlockedDecrement(&old->ref_count) == 0) old->ReleaseWhenZero();
            m_object34 = replacement;
            if (replacement != 0) InterlockedIncrement(&replacement->ref_count);
        }
        m_object34->Finalize();
    }
}