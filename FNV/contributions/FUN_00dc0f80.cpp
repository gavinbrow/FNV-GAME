struct Allocator {
 virtual void slot0(); virtual void slot1(); virtual void Free(void*, unsigned);
};
struct Manager { unsigned flags, state, count, capacity; Allocator* allocator; };
Manager* FUN_00c85750();
struct FUN_00dc0f80 {
 unsigned short allocationSize;
 FUN_00dc0f80();
 virtual ~FUN_00dc0f80();
 void operator delete(void* ptr) {
  Manager* manager = FUN_00c85750();
  manager->allocator->Free(ptr, static_cast<FUN_00dc0f80*>(ptr)->allocationSize);
 }
};
FUN_00dc0f80::FUN_00dc0f80() {}



