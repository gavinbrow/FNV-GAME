class MemoryManager
{
public:
    void Deallocate(void* pointer);
};
extern char DAT_010a28c8;
extern MemoryManager DAT_011f6238;
struct FUN_00aa7840_cls
{
    void* m_vftable;
    void* FUN_00aa7840(unsigned int deleteFlags);
};
// @fnv 0x00aa7840
void* FUN_00aa7840_cls::FUN_00aa7840(unsigned int deleteFlags)
{
    m_vftable = &DAT_010a28c8;
    if ((deleteFlags & 1) != 0)
    {
        DAT_011f6238.Deallocate(this);
    }
    return this;
}