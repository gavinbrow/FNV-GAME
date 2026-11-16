extern void* __cdecl FUN_00aa13e0(unsigned int size);
struct CopyMembersArguments {
    NiBlendFloatInterpolator* destination;
    void* cloningProcess;
};
extern "C" void __fastcall FUN_00a37510(void* source, CopyMembersArguments args);

struct BlendFloatSource : NiBlendFloatInterpolator {
    NiBlendFloatInterpolator* __thiscall FUN_00a405f0(void* cloning);
};

NiBlendFloatInterpolator* BlendFloatSource::FUN_00a405f0(void* cloning) {
    NiBlendFloatInterpolator* copy =
        static_cast<NiBlendFloatInterpolator*>(FUN_00aa13e0(sizeof(NiBlendFloatInterpolator)));
    if (copy) {
        FUN_00a36890(copy);
        *reinterpret_cast<const void***>(copy) = vftable_NiBlendFloatInterpolator;
        copy->m_fFloatValue = DAT_0109a918;
    } else {
        copy = 0;
    }
    CopyMembersArguments args = {copy, cloning};
    FUN_00a37510(this, args);
    copy->m_fFloatValue = m_fFloatValue;
    return copy;
}
