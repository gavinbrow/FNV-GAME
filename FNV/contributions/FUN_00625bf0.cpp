struct FUN_00625bf0_Item {
    void* unk00;
    void* unk04;
};
struct FUN_00625bf0_Container {
    int FUN_00726070();
    FUN_00625bf0_Item* FUN_00626660(int index);
};
void __cdecl FUN_00626760(void* object);
struct FUN_00625bf0_Class {
    void FUN_00625bf0(FUN_00625bf0_Container* container);
};
void FUN_00625bf0_Class::FUN_00625bf0(FUN_00625bf0_Container* container)
{
    for (int index = 0; index < container->FUN_00726070(); ++index) {
        FUN_00625bf0_Item item = *container->FUN_00626660(index);
        FUN_00626760(item.unk00);
    }
}