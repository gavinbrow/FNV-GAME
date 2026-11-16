struct FUN_00aadda0_Class {
    void __thiscall FUN_00658260(int a, float b);
    int __thiscall FUN_00aadda0(int a, float b);
};

int FUN_00aadda0_Class::FUN_00aadda0(int a, float b) {
    int flags = 0;
    FUN_00658260(a, 1.0f / b);
    flags |= 1;
    return a;
}
