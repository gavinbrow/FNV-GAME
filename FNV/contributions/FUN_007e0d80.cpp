struct FUN_007e0d80_shell : Flt {
    char* m_buffer;
    unsigned int FUN_004048e0();
    unsigned int FUN_004039a0();
    void FUN_004037f0(char* oldBuffer, unsigned int requiredLength);
    void FUN_004039c0(unsigned int newLength);
    unsigned int FUN_004f4280();
    void FUN_00438470(FUN_007e0d80_shell* other);
    FUN_007e0d80_shell* FUN_007e0d80(FUN_007e0d80_shell* other);
};
extern "C" void* __cdecl memcpy(void*, const void*, unsigned int);

FUN_007e0d80_shell* FUN_007e0d80_shell::FUN_007e0d80(FUN_007e0d80_shell* other)
{
    if ((unsigned int)*other) {
        if ((unsigned int)*this) {
            unsigned int newLength = FUN_004048e0() + other->FUN_004048e0();
            if (newLength > FUN_004039a0()) {
                FUN_004037f0((char*)(unsigned int)*this, newLength);
            }
            memcpy(m_buffer + FUN_004048e0(),
                   (char*)(unsigned int)*other,
                   other->FUN_004f4280());
            FUN_004039c0(newLength);
        } else {
            FUN_00438470(other);
        }
    }
    return this;
}