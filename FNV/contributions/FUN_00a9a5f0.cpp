struct NiCloningProcess;
struct NiCullingProperty : NiProperty {
    void* vtable;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    unsigned short unk18;
    void FUN_00a5d7a0(NiCullingProperty*, NiCloningProcess&);
    NiCullingProperty* FUN_00a9a5f0(NiCloningProcess&);
};
NiCullingProperty* NiCullingProperty::FUN_00a9a5f0(NiCloningProcess& process) {
    NiCullingProperty* copy = (NiCullingProperty*)BSFadeNode::operator new(0x1c);
    if (copy) {
        copy->FUN_00a9a640_ctor();
        copy->vtable = &DAT_010a0f6c;
        copy->unk18 = 0;
    } else {
        copy = 0;
    }
    FUN_00a5d7a0(copy, process);
    copy->unk18 = unk18;
    return copy;
}
