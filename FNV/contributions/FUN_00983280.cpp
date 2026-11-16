struct StageHolder;
struct MapMember {
    void FUN_00aa6060();
    void FUN_00aa62e0();
};
struct HolderLookup {
    bool FUN_00853130(unsigned int key, void** value);
    void FUN_00844700(unsigned int key, void* value);
};
struct CreatedShell {
    unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0c;
    unsigned int unk10; unsigned int unk14; unsigned int unk18;
    CreatedShell();
    void FUN_00983400(unsigned char value);
    void FUN_00982e70(int value, StageHolder* holder);
};
struct HolderStatus {
    bool GetDone();
    void FUN_0067fdb0(unsigned char value);
};
void FUN_00983280_holder::FUN_00983280(int value, StageHolder* holder) {
    ((MapMember*)((char*)this + 0x14))->FUN_00aa6060();
    void* object = 0;
    if (!((HolderLookup*)this)->FUN_00853130(*(unsigned int*)((char*)holder + 0x68), &object)) {
        object = new CreatedShell();
        ((CreatedShell*)object)->FUN_00983400(((HolderStatus*)holder)->GetDone());
        ((HolderLookup*)this)->FUN_00844700(*(unsigned int*)((char*)holder + 0x68), object);
    }
    ((CreatedShell*)object)->FUN_00982e70(value, holder);
    ((HolderStatus*)holder)->FUN_0067fdb0(1);
    ((MapMember*)((char*)this + 0x14))->FUN_00aa62e0();
}