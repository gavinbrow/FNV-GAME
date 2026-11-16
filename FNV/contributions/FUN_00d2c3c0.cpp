struct Block { Block* next; };
struct Allocator {
    virtual void v0();
    virtual void* Allocate(int size);
    virtual void v2(); virtual void v3(); virtual void v4(); virtual void v5();
    virtual void AllocateBatch(Block** output, int count, int size);
};
struct Cache { Block* head; volatile int count; };
struct BlockCache {
    void* owner;
    Allocator* allocator;
    int batchCount;
    Cache caches[17];
    int blockSizes[17];
    void* FUN_00d2c3c0(int index);
    __forceinline void* AllocateBatchCached(int index, int count) {
    Block* blocks[4];
    if (count >= 4) count = 4;
    allocator->AllocateBatch(blocks, count, blockSizes[index]);
    for (int i = 1; i < count; ++i) {
        Block* block = blocks[i];
        Block* previous = caches[index].head;
        ++caches[index].count;
        block->next = previous;
        caches[index].head = block;
    }
    return blocks[0];
    }
};
void* BlockCache::FUN_00d2c3c0(int index) {
    int count = batchCount;
    if (!count) return allocator->Allocate(blockSizes[index]);
    return AllocateBatchCached(index, count);
}

