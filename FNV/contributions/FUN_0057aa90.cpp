struct AttachedResource { unsigned int FUN_009ad610(); };
struct InterfaceObject {
    virtual void slot0();
    virtual void slot4();
    virtual void slot8();
    virtual void slotC();
    virtual AttachedResource* getResource();
};
struct ResourceHandle { InterfaceObject* FUN_00559450(); };
struct ResourceOwner { unsigned int FUN_008d6f30(); };
struct RegistryWithMethod : GlobalObject_00559cc0 {
    void FUN_00844700(unsigned int resource, ResourceOwner* owner);
};
unsigned char __cdecl FUN_0057ab50(void* resource);
struct FUN_0057aa90_Class {
    void* unk00; void* unk04; void* unk08; void* unk0C;
    void* unk10; void* unk14;
    ResourceOwner* owner18;
    ResourceHandle resource1C;
    void* unk20;
    unsigned char enabled24;
    void FUN_0057aa90();
};
void FUN_0057aa90_Class::FUN_0057aa90()
{
    if (enabled24) {
        unsigned int index;
        AttachedResource* candidate;
        candidate = resource1C.FUN_00559450()
            ? resource1C.FUN_00559450()->getResource()
            : 0;
        index = candidate ? candidate->FUN_009ad610() : 0;
        if (index && owner18->FUN_008d6f30()) {
            owner18->FUN_008d6f30();
            if (FUN_0057ab50(reinterpret_cast<void*>(index))) {
                reinterpret_cast<RegistryWithMethod&>(g_011ca304).FUN_00844700(index, owner18);
            }
        }
    }
}