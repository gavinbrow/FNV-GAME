struct Inner {
    void FUN_00a698a0(void* target);
};
struct Outer {
    int unk00;
    Inner inner04;
};
void __cdecl FUN_00a3da50(void* target, Outer* source);
void __cdecl FUN_00a29660(void* target, Outer* source)
{
    FUN_00a3da50(target, source);
    source->inner04.FUN_00a698a0(target);
}