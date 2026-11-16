void __cdecl FUN_00a3d630(unsigned int mode, NiAnimationKey::KeyType type,
    NiBoolKey* sourceKeys, unsigned int sourceCount,
    float startTime, float endTime, NiBoolKey** outputKeys, unsigned int* outputCount);

struct FUN_00a53910_shell : NiBoolData
{
    void __thiscall FUN_00a5d510(NiBoolData*& clone);
    void __thiscall FUN_00a53910(float startTime, float endTime, NiPointer<NiBoolData>& output);
};

void FUN_00a53910_shell::FUN_00a53910(float startTime, float endTime,
                                       NiPointer<NiBoolData>& output)
{
    NiBoolData* original = 0;
    FUN_00a5d510(original);

    NiBoolData* copy = original;
    if (copy != 0)
        copy->IncRefCount();

    if (m_uiNumKeys > 0)
    {
        NiBoolKey* keys = 0;
        unsigned int count = 0;
        FUN_00a3d630(5, m_eType, m_pkKeys, m_uiNumKeys,
                      startTime, endTime, &keys, &count);
        copy->ReplaceAnim(keys, count, m_eType);
    }

    NiBoolData* previous = output.m_pObject;
    if (previous != copy)
    {
        if (previous != 0)
            previous->DecRefCount();

        output.m_pObject = copy;
        if (copy != 0)
            copy->IncRefCount();
    }
    if (copy != 0)
        copy->DecRefCount();
    if (original != 0)
        original->DecRefCount();
}
