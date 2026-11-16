struct Entry { unsigned short type; unsigned short index; };
struct Container {
    Entry* entries;
    int count;
    int capacity;
    void FUN_00d1a040(int indexOffset, int** remap);
};
void __cdecl FUN_00c908c0(void*, void*, int, int);
extern unsigned char* DAT_011b37a4[2];
void Container::FUN_00d1a040(int indexOffset, int** remap) {
    Entry* src = entries;
    Entry* end = src + count;
    int kept = 0;
    Entry* dst = src;
    while (src < end) {
        int mapped = (*remap)[src->index];
        if (mapped >= 0) {
            *dst = *src;
            dst->index = (unsigned short)mapped;
            *(unsigned short*)((char*)DAT_011b37a4[src->type & 1] + mapped * 16 + indexOffset) = (unsigned short)kept;
            ++dst;
            ++kept;
        }
        ++src;
    }
    BSAudio* audio = FUN_00c85750();
    void* mgr = ((void**)audio)[4];
    int capacity = this->capacity & 0x3fffffff;
    if (capacity < kept) {
        int newCapacity = capacity * 2;
        if (kept >= newCapacity)
            newCapacity = kept;
        FUN_00c908c0(mgr, this, newCapacity, 4);
    }
    count = kept;
}