void* __cdecl operator new(unsigned int size, void* where);
void __cdecl operator delete(void*, void*);
struct FUN_0049f1c0 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    FUN_0049f1c0();
    ~FUN_0049f1c0();
};
void FUN_0049fbf0_class::FUN_0049fb50(void* elements, unsigned int count) {
    for (unsigned int index = 0; index < count; ++index) {
        new (static_cast<char*>(elements) + index * 16) FUN_0049f1c0;
    }
}