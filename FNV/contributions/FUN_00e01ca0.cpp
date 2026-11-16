struct Allocator {
 virtual void Allocate();
 virtual void Reallocate();
 virtual void Free(void* object, unsigned int size);
};
struct AudioManager {
 int unk00; int unk04; int unk08; int unk0c;
 Allocator* allocator;
};
AudioManager* FUN_00c85750();
struct AudioObject {
 void* vtable;
 unsigned short allocationSize;
 void FUN_00e4a750();
 AudioObject* FUN_00e01ca0(unsigned int flags);
};
AudioObject* AudioObject::FUN_00e01ca0(unsigned int flags)
{
 FUN_00e4a750();
 if (flags & 1) {
  AudioManager* manager = FUN_00c85750();
  manager->allocator->Free(this, allocationSize);
 }
 return this;
}
