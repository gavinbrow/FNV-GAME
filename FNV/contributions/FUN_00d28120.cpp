inline void* __cdecl operator new(unsigned int, void* p) { return p; }
struct IndexBuffer { int* data; int size; unsigned capacityFlags; };
struct IndexStorage { int* data; };
struct AllocationManager { int unk00; int unk04; int unk08; int unk0C; void* allocator; };
AllocationManager* __cdecl FUN_00c85750();
void __cdecl FUN_00c90940(void*, IndexBuffer*, int);
struct IndexRemapper { IndexStorage* entries; int length; void FUN_00d280e0(); void FUN_00d28120(IndexBuffer*); };
void IndexRemapper::FUN_00d28120(IndexBuffer* output) {
 FUN_00d280e0(); int nextIndex=0;
 for(int i=0;i<length;++i) {
  int* values=entries->data; int value=values[i];
  if(value<0) {
   value=-value;
   AllocationManager* manager=FUN_00c85750();
   if(output->size == (output->capacityFlags & 0x3fffffffU)) FUN_00c90940(manager->allocator,output,4);
   int* slot = output->data + output->size; __assume(slot != 0); new (slot) int(value);
   ++output->size; entries->data[i]=nextIndex++;
  } else { values[i]=values[value]; }
 }
}