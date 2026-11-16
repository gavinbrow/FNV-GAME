struct MemoryManager
{
    void Deallocate(void* memory);
};

extern MemoryManager DAT_011f6238;

struct FUN_00aa74c0
{
    virtual ~FUN_00aa74c0();
    void* FUN_00aa77e0(unsigned int flags);
};

// @fnv 0x00aa77e0
void* FUN_00aa74c0::FUN_00aa77e0(unsigned int flags)
{
    this->FUN_00aa74c0::~FUN_00aa74c0();
    if (flags & 1)
    {
        DAT_011f6238.Deallocate(this);
    }
    return this;
}
