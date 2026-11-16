extern "C" __declspec(dllimport) int __stdcall ReleaseSemaphore(void* h, long releaseCount, long* previousCount);
struct FUN_00d04390 { void* handle; unsigned long wait(unsigned long amount); };
unsigned long FUN_00d04390::wait(unsigned long amount) { return (unsigned long)ReleaseSemaphore(*(void**)this, (long)amount, 0); }
