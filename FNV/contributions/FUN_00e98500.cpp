struct VBLayout;
struct VBArray {
    unsigned int m_uiCount;
    VBLayout** m_pData;
    void FUN_00ba3aa0(unsigned int, VBLayout**);
};
struct VBLayout {
    void* m_pkSet;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int m_uiSize;
    unsigned int unk10;
    unsigned int m_uiOffset;
    VBLayout* m_pkNext;
    VBLayout* m_pkPrev;
    unsigned int m_uiCurrOffset;
    unsigned int m_uiFreeBytes;
    unsigned int m_uiTotalFreeBytes;
    VBArray m_apkBlocks;
};
extern VBLayout* g_pkFreeList;
unsigned int __fastcall FUN_00e98500(NiVBBlock* object, void*, unsigned int index)
{
    VBLayout* self = reinterpret_cast<VBLayout*>(object);
    unsigned int result = 0;
    VBLayout* block = self->m_apkBlocks.m_pData[index];
    if (block) {
        result = block->m_uiOffset;
        if (self->m_uiCurrOffset - result == block->m_uiSize) {
            self->m_uiCurrOffset = 0;
            if (index > 0) {
                VBLayout** cursor = self->m_apkBlocks.m_pData;
                unsigned int remain = index;
                do {
                    VBLayout* current = *cursor;
                    if (current) {
                        unsigned int end = current->m_uiOffset + current->m_uiSize;
                        if (end > self->m_uiCurrOffset)
                            self->m_uiCurrOffset = end;
                    }
                    ++cursor;
                } while (--remain);
            }
        }
        self->m_uiFreeBytes = self->m_uiSize - self->m_uiCurrOffset;
        self->m_uiTotalFreeBytes += result;
        VBLayout* removed = 0;
        self->m_apkBlocks.FUN_00ba3aa0(index, &removed);
        block->m_pkPrev = 0;
        block->m_pkNext = g_pkFreeList;
        if (g_pkFreeList)
            g_pkFreeList->m_pkPrev = block;
        g_pkFreeList = block;
    }
    return result;
}