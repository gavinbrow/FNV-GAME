struct FUN_00432da0_object {
    void FUN_004d9380();
    void* FUN_00432da0(unsigned int flags);
};
void __cdecl operator delete(void*);
void* FUN_00432da0_object::FUN_00432da0(unsigned int flags) {
    FUN_004d9380();
    if (flags & 1) {
        operator delete(this);
    }
    return this;
}