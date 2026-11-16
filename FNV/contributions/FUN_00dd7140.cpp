struct FreeNode { FreeNode* next; };
struct FreeBlock { FreeBlock* next; unsigned int unk04; unsigned int m_begin; unsigned int m_count; };
struct HavokBool { unsigned char value; HavokBool(bool v) : value(v) {} operator bool() const { return value != 0; } };
struct FreeAllocator {
    virtual void unknown00();
    virtual void unknown04();
    virtual void unknown08();
    virtual HavokBool TestBlock(FreeBlock* block);
};
struct FreeListCheck {
    FreeNode* m_freeHead; unsigned int m_elementSize; unsigned int unk08;
    FreeBlock* m_blocks; unsigned int unk10; unsigned int unk14;
    unsigned int m_alignment; unsigned int unk1C; unsigned int unk20; unsigned int unk24;
    unsigned int unk28; unsigned int unk2C; FreeAllocator* m_allocator;
    bool* FUN_00dd7140(bool* result);
};
bool* FreeListCheck::FUN_00dd7140(bool* result)
{
    FreeNode* item = m_freeHead;
    while (item != 0)
    {
        if ((reinterpret_cast<unsigned int>(item) & (m_alignment - 1)) != 0)
            goto invalid;
        FreeBlock* block = m_blocks;
        if (block == 0)
            goto invalid;
        do
        {
            if (!m_allocator->TestBlock(block))
                goto invalid;
            unsigned int base = block->m_begin;
            unsigned int addr = reinterpret_cast<unsigned int>(item);
            if (addr >= base && addr < base + block->m_count * m_elementSize)
            {
                if ((addr - base) % m_elementSize != 0)
                    goto invalid;
                break;
            }
            block = block->next;
        } while (block != 0);
        if (block == 0)
            goto invalid;
        item = item->next;
    }
    *result = true;
    return result;
invalid:
    *result = false;
    return result;
}