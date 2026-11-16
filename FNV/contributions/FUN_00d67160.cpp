struct Prefix32 {
    int unk00; int unk04; int unk08; int unk0C;
    int unk10; int unk14; int unk18; int unk1C;
};
struct SecondaryBase {
    void FUN_00d67160();
};
struct CompleteObject : Prefix32, SecondaryBase {
    void FUN_00d67020();
};
void SecondaryBase::FUN_00d67160() {
    CompleteObject* object = reinterpret_cast<CompleteObject*>(reinterpret_cast<char*>(this) - sizeof(Prefix32));
    object->FUN_00d67020();
}
