void __cdecl operator delete(void*);

struct FUN_00651b00_class {
    void FUN_006518e0();
    FUN_00651b00_class* FUN_00651b00(unsigned int flags);
};

FUN_00651b00_class* FUN_00651b00_class::FUN_00651b00(unsigned int flags) {
    FUN_006518e0();
    if (flags & 1) {
        ::operator delete(this);
    }
    return this;
}
