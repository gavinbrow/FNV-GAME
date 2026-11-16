void* __cdecl operator new(unsigned int size);
struct FUN_0048a3d0;
typedef void (__thiscall *CopyMethod)(FUN_0048a3d0*, const FUN_0048a3d0*);
typedef void* (__thiscall *ReleaseMethod)(FUN_0048a3d0*, int);
struct EffectMethods {
    void* unk00;
    void* unk04;
    CopyMethod copy08;
    void* unk0c;
    ReleaseMethod release10;
};
struct FUN_0048a3d0 {
    EffectMethods* methods;
    int unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    FUN_0048a3d0();
};
struct CopyInterface {
    virtual void unknown00();
    virtual void unknown04();
    virtual void CopyFrom(const FUN_0048a3d0* other);
};
struct EffectData {
    unsigned char flags00;
    unsigned char flags01;
    unsigned char flags02;
    int count04;
    int count08;
    int count0c;
    int count10;
    FUN_0048a3d0* effect14;
    void FUN_00478fd0(const EffectData* source);
};
void EffectData::FUN_00478fd0(const EffectData* source)
{
    if (!source)
        return;
        flags01 = source->flags01;
        count04 = source->count04;
        flags00 = source->flags00;
        flags02 = source->flags02;
        count08 = source->count08;
        count0c = source->count0c;
        count10 = source->count10;
        if (effect14)
        {
            FUN_0048a3d0* oldEffect = effect14;
            FUN_0048a3d0* previous = oldEffect;
            previous ? previous->methods->release10(previous, 1) : 0;
            effect14 = 0;
        }
        if (source->effect14)
        {
            effect14 = new FUN_0048a3d0();
            reinterpret_cast<CopyInterface*>(effect14)->CopyFrom(source->effect14);
        }
}
