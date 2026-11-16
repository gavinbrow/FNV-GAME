// Fallout: New Vegas — FUN_00c85620
// __cdecl aligned-allocation helper: requests an over-sized block from the
// heap object's virtual allocator, aligns the returned pointer up to the
// requested alignment, and stores a small header immediately below the
// aligned pointer: {owner, end, offset-to-raw}.

struct FUN_00c85620_heap
{
    virtual void v0();
    virtual void* Allocate(unsigned int uiSize);
};

void* __cdecl FUN_00c85620(FUN_00c85620_heap* pkHeap, unsigned int uiSize, unsigned int uiAlignment)
{
    unsigned int uiEnd = uiSize + uiAlignment;
    void* pvRaw = pkHeap->Allocate(uiEnd + 0x10);

    unsigned int uiAligned = (unsigned int)pvRaw + uiAlignment + 0xf;
    uiAligned &= ~(uiAlignment - 1);

    unsigned int* puiBlock = (unsigned int*)uiAligned;
    puiBlock[-3] = uiEnd;
    puiBlock[-4] = (unsigned int)pkHeap;
    puiBlock[-2] = uiAligned - (unsigned int)pvRaw;

    return (void*)uiAligned;
}
