struct FUN_00d7caa0_class {
    void __thiscall FUN_00d7caa0(float, int);
};

struct FUN_00d76920_class {
    void* m_00;
    void* m_04;
    FUN_00d7caa0_class* m_08;
    void FUN_00d76920(float, int);
};

void __thiscall FUN_00d76920_class::FUN_00d76920(float f, int i) {
    m_08->FUN_00d7caa0(f, i);
}
