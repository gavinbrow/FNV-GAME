struct Callback {
    void (__cdecl *onPrimary)(Callback*);
    void (__cdecl *onSecondary)(Callback*);
};
struct CallbackCollection {
    unsigned int FUN_0044ddc0();
    Callback** FUN_006a7ad0(unsigned int index);
};
void FUN_007c9dc0_Class::FUN_007cacd0()
{
    if (*reinterpret_cast<int*>(reinterpret_cast<char*>(this) + 0x48) < 9) {
        for (unsigned int i = 0; i < reinterpret_cast<CallbackCollection*>(
                reinterpret_cast<char*>(this) + 0x70 +
                (*reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x48) << 5)
            )->FUN_0044ddc0(); ++i) {
            (*reinterpret_cast<CallbackCollection*>(
                reinterpret_cast<char*>(this) + 0x70 +
                (*reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x48) << 5)
            )->FUN_006a7ad0(i))->onPrimary(
                *reinterpret_cast<CallbackCollection*>(
                    reinterpret_cast<char*>(this) + 0x70 +
                    (*reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x48) << 5)
                )->FUN_006a7ad0(i)
            );
        }
        for (unsigned int j = 0; j < reinterpret_cast<CallbackCollection*>(
                reinterpret_cast<char*>(this) + 0x60 +
                (*reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x48) << 5)
            )->FUN_0044ddc0(); ++j) {
            (*reinterpret_cast<CallbackCollection*>(
                reinterpret_cast<char*>(this) + 0x60 +
                (*reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x48) << 5)
            )->FUN_006a7ad0(j))->onSecondary(
                *reinterpret_cast<CallbackCollection*>(
                    reinterpret_cast<char*>(this) + 0x60 +
                    (*reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x48) << 5)
                )->FUN_006a7ad0(j)
            );
        }
    }
}