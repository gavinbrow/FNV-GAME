struct MemoryAllocator { virtual void v0(); virtual void v1(); virtual void Free(void* memory, unsigned int size); };
struct AllocatorHolder { int unk00; int unk04; int unk08; int unk0c; MemoryAllocator* allocator; };
extern AllocatorHolder* __cdecl FUN_00c85750();
struct StreamStatisticsCollector { int unk00; unsigned short unk04; void FUN_00ddf240(); void* FUN_00ddfb40(unsigned int flags); };
void* StreamStatisticsCollector::FUN_00ddfb40(unsigned int flags) {
 FUN_00ddf240();
 if (flags & 1) {
  AllocatorHolder* holder = FUN_00c85750();
  holder->allocator->Free(this, (unsigned int)unk04);
 }
 return this;
}
