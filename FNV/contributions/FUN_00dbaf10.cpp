struct FUN_00dbaf10_callback {
    virtual void f0(); virtual void f1(); virtual void f2(); virtual void f3();
    virtual void f4(); virtual void f5(); virtual void f6();
    virtual void dispatch(int index, void* record);
};
struct FUN_00dbaf10_cls {
    FUN_00dbaf10_callback* vtbl;
    void* p1;
    void* p2;
    int __thiscall FUN_00dba6f0();
    void __thiscall FUN_00dbaf10(void* records);
};
void __thiscall FUN_00dbaf10_cls::FUN_00dbaf10(void* records) {
    int count = FUN_00dba6f0();
    int index = 0;
    if (count > 0) {
        int offset = 0;
        do {
            vtbl->dispatch(index, (char*)*(void**)records + offset);
            ++index;
            offset += 20;
        } while (index < count);
    }
}

