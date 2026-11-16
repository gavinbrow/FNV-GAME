struct FUN_00a5e3a0_Helper { void* FUN_00aa3e40(unsigned int); };
struct NiStandardAllocator { static void* __cdecl operator new(unsigned int); virtual void func(); };
void* __cdecl NiStandardAllocator::operator new(unsigned int n) {
    return ((FUN_00a5e3a0_Helper*)&g_memoryManager)->FUN_00aa3e40(n);
}
struct FUN_00aa2200 { NiStandardAllocator* object; unsigned char initialized; FUN_00aa2200(); };
FUN_00aa2200::FUN_00aa2200() {
    object = new NiStandardAllocator;
    initialized = 1;
}
