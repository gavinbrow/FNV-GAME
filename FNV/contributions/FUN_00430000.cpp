void* __cdecl operator new(unsigned int, void*);
void __cdecl operator delete(void*, void*);
struct FUN_004300a0 {
    void* m_value;
    FUN_004300a0();
};
void BSSimpleArrayShell_FUN_00430000::FUN_00430000(void* data, unsigned int count)
{
    for (unsigned int index = 0; index < count; ++index) {
        new (&static_cast<FUN_004300a0*>(data)[index]) FUN_004300a0;
    }
}