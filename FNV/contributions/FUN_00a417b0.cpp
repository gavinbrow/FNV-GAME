struct MorphBuffer { void* unk00; unsigned int used; void* unk08; int (__cdecl *append)(MorphBuffer*, void*, unsigned int, const unsigned int*, int); };
static __forceinline unsigned int countBytes(const volatile unsigned int& count) { return count * 4; }
void __cdecl FUN_00a417b0(void* owner, void* source, unsigned int elementCount){
 MorphBuffer* __restrict buffer = *reinterpret_cast<MorphBuffer**>(reinterpret_cast<char*>(owner)+0x250);
 unsigned int stride=4;
 buffer->used += buffer->append(buffer,source,countBytes(elementCount),&stride,1);
}
