
void __cdecl operator delete(void* pointer);

struct FUN_0081db60_shell {
    void FUN_0081db90();
    FUN_0081db60_shell* FUN_0081db60(unsigned int deletingFlags);
};

FUN_0081db60_shell* FUN_0081db60_shell::FUN_0081db60(unsigned int deletingFlags) {
    FUN_0081db90();
    if (deletingFlags & 1) {
        ::operator delete(this);
    }
    return this;
}
