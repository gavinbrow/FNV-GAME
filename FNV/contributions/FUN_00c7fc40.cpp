struct FNVHeapAllocator {
    void* FUN_00aa4150(void* address, unsigned int bytes);
};
extern FNVHeapAllocator DAT_011f6238;

void* __stdcall FUN_00c7fc40(void* address, unsigned int elementCount) {
    return DAT_011f6238.FUN_00aa4150(address, elementCount * sizeof(double));
}
