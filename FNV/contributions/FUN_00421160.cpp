extern char DAT_010151f0;
void __cdecl FUN_00401030(void* pointer);

struct FUN_00421160_shell {
    void* m_vftable;
    void* unk04;
    void* unk08;
    void* m_pChanges;
    void FUN_0040ecb0();
    void FUN_00421160();
};

void FUN_00421160_shell::FUN_00421160()
{
    m_vftable = &DAT_010151f0;
    void* changes = m_pChanges;
    FUN_00401030(changes);
    FUN_0040ecb0();
}
