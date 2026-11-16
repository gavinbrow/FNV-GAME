struct ArrayBlock { unsigned int* values; int size; unsigned int reservedAndFlags; };
struct AllocatorState {
 int unk00,unk04,unk08,unk0C;
 void* pool;
 void* GetPool() const { return pool; }
};
extern "C" AllocatorState* __cdecl FUN_00c85750();
extern "C" void __cdecl FUN_00c908c0(void*, ArrayBlock*, int, int);
struct ArrayHost { int unk00,unk04,unk08; ArrayBlock array; void FUN_00dc9bd0(int desired); };
void ArrayHost::FUN_00dc9bd0(int desired) {
 ArrayBlock* values = &array;
 void* pool = FUN_00c85750()->GetPool();
 int capacity = values->reservedAndFlags & 0x3fffffff;
 if (capacity < desired) {
   int nextCapacity = capacity * 2;
   if (desired >= nextCapacity) nextCapacity = desired;
   FUN_00c908c0(pool, values, nextCapacity, 4);
 }
 int extra = desired - values->size;
 unsigned int* next = values->values + values->size;
 while (extra > 0) { *next++ = 0; --extra; }
 values->size = desired;
}