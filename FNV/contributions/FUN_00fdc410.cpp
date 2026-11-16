struct MemoryManager { void Deallocate(void*); };
extern MemoryManager g_memoryManager;
struct FUN_00483710 { ~FUN_00483710() {} };
struct Base : FUN_00483710 { void* ptr; ~Base() { void* v = ptr; g_memoryManager.Deallocate(v); } };
struct FUN_00b0e1a0 : Base { ~FUN_00b0e1a0() {} };
struct G : FUN_00b0e1a0 { void FUN_00b0e7f0(); ~G() { char pad[24]; FUN_00b0e7f0(); } };
G DAT_011f8bdc;
