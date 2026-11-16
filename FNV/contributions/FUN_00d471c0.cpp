struct FUN_00d86980_class {
    int __thiscall FUN_00d86980();
};
struct FUN_00d471c0_target {
    virtual void vf00();
    virtual void vf04();
    virtual void vf08();
    virtual void vf0c();
    virtual void vf10(int a, int b);
};
struct FUN_00d47130_class {
    int FUN_00d47130(const char* name, int* out, FUN_00d86980_class** pp);
    int __thiscall FUN_00d471c0(const char* name, FUN_00d471c0_target* target);
};
int __thiscall FUN_00d47130_class::FUN_00d471c0(const char* name, FUN_00d471c0_target* target)
{
    int index;
    FUN_00d86980_class* p;
    int result = FUN_00d47130(name, &index, &p);
    if (result == 0)
        target->vf10(index, p->FUN_00d86980());
    return result;
}