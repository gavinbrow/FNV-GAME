struct FUN_00527990_shell {
    bool FUN_00527990(int* first, int* second);
};
struct FUN_006dd280_shell {
    void FUN_006dd280(BGSPerk** item, int value, void* data);
};
struct FUN_006dd220_Class {
    FUN_006dd220_Class* FUN_006dd220(void* source);
};
FUN_006dd220_Class* FUN_006dd220_Class::FUN_006dd220(void* source)
{
    *reinterpret_cast<int**>(this) = &DAT_0102583c;
    reinterpret_cast<BSSimpleList<BGSPerk*>*>(reinterpret_cast<char*>(this) + 4)->GetItem();
    int b = 0;
    int a = 0;
    reinterpret_cast<FUN_00527990_shell*>(source)->FUN_00527990(&b, &a);
    reinterpret_cast<FUN_006dd280_shell*>(this)->FUN_006dd280(
        &reinterpret_cast<BSSimpleList<BGSPerk*>*>(source)->GetItem(),
        b, reinterpret_cast<void*>(a));
    return this;
}