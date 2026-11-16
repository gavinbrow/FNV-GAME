struct hkReferencedObject {
    __declspec(nothrow) void removeReference();
};
struct FUN_00e02d40_helper {
    __declspec(nothrow) void FUN_00e02d40();
};
struct FUN_00e02c70_audio_iface {
    virtual __declspec(nothrow) void v0();
    virtual __declspec(nothrow) void v1();
    virtual __declspec(nothrow) void v2(void* object, unsigned int value);
};
struct FUN_00e02c70_audio_holder {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00e02c70_audio_iface* unk10;
};
void* __cdecl FUN_00c85750();
struct BaseE02c70 {
    int unk04;
    virtual __declspec(nothrow) ~BaseE02c70() {}
};
struct FUN_00e02c70_Class : BaseE02c70 {
    hkReferencedObject* unk08;
    FUN_00e02d40_helper* unk0c;
    virtual __declspec(nothrow) ~FUN_00e02c70_Class();
};
FUN_00e02c70_Class::~FUN_00e02c70_Class() {
    hkReferencedObject* reference = unk08;
    reference->removeReference();
    FUN_00e02d40_helper* member = unk0c;
    if (member) {
        member->FUN_00e02d40();
        FUN_00e02c70_audio_holder* audio = (FUN_00e02c70_audio_holder*)FUN_00c85750();
        audio->unk10->v2(member, 0x24);
    }
}


