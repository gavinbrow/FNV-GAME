struct AudioAllocator {
 virtual void Reserved0();
 virtual void Reserved1();
 virtual void Release(void*, unsigned int);
};
struct BSAudio {
 unsigned int unk00, unk04, unk08, unk0C;
 AudioAllocator* allocator;
 void Release(void* p, unsigned int size) { allocator->Release(p, size); }
};
BSAudio* FUN_00c85750();
struct AudioObject {
 unsigned int unk00;
 unsigned short allocationSize;
 void FUN_00e023c0();
 static void operator delete(void* p) { BSAudio* audio = FUN_00c85750(); AudioObject* object = static_cast<AudioObject*>(p); audio->allocator->Release(p, object->allocationSize); }
 void* FUN_00e02430(unsigned int flags);
};
void* AudioObject::FUN_00e02430(unsigned int flags) {
 FUN_00e023c0();
 if (flags & 1) operator delete(this);
 return this;
}

