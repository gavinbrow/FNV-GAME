struct FreeNode { FreeNode* next; };
struct FreeBlock { FreeNode* head; int count; };
struct OverflowHandler { virtual void f0(); virtual FreeNode* f1(int); };
struct Allocator : FUN_00d2c3a0_class {
    FreeBlock blocks[25];
    int unkD4;
    signed char bucketForSmallSize[44];
    int bucketForLargeSize[8];
    FreeNode* FUN_00d2c5a0(int size);
};
// The target helper ignores EDX; this ABI-compatible signature keeps its this pointer in ECX and bucket on the stack.
extern "C" FreeNode* __fastcall FUN_00d2c3c0(Allocator* self, int unused, int bucket);
FreeNode* Allocator::FUN_00d2c5a0(int size) {
    if (size <= 0x2000) {
        int bucket;
        if (size <= 0x280)
            bucket = bucketForSmallSize[(size + 0xf) >> 4];
        else
            bucket = bucketForLargeSize[(size - 1) >> 10];
        FreeBlock* block = &blocks[bucket];
        if (block->head) {
            FreeNode* node = block->head;
            --block->count;
            block->head = node->next;
            return node;
        }
        return FUN_00d2c3c0(this, bucket, bucket);
    }
    return ((OverflowHandler*)m4)->f1(size);
}



