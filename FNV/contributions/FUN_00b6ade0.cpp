void* __cdecl FUN_00aa13e0(unsigned int size);
struct FUN_00b6abb0 {
    FUN_00b6abb0();
    static void* operator new(unsigned int size, unsigned int requestedSize) {
        return FUN_00aa13e0(requestedSize);
    }
    unsigned int m_type;
};
struct EntityManagerB6 {
    void FUN_00b6a6c0(FUN_00b6abb0* object, int context);
    FUN_00b6abb0* FUN_00b6ade0(int context);
};
FUN_00b6abb0* EntityManagerB6::FUN_00b6ade0(int context) {
    FUN_00b6abb0* object = new (0x150) FUN_00b6abb0();
    FUN_00b6a6c0(object, context);
    return object;
}
