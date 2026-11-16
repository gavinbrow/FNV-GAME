extern MemoryManager g_memoryManager;

struct ShaderState {
    void __thiscall FUN_00a615c0();
    ~ShaderState() { FUN_00a615c0(); }
    static void operator delete(void* p) { g_memoryManager.Deallocate(p); }
};
struct ShaderEntry {
    void __thiscall FUN_00a61ec0();
};
extern ShaderState* DAT_011f4468;
extern unsigned char* DAT_011f4464;
void __cdecl FUN_00a62030();

void __cdecl FUN_00a62090()
{
    FUN_00a62030();

    delete DAT_011f4468;

    unsigned char* entries = DAT_011f4464;
    DAT_011f4468 = 0;
    if (entries != 0) {
        int count = *reinterpret_cast<int*>(entries - 4);
        unsigned char* current = entries + count * 2856;
        int* allocation = reinterpret_cast<int*>(entries - 4);
        if (--count >= 0) {
            do {
                current -= 2856;
                reinterpret_cast<ShaderEntry*>(current)->FUN_00a61ec0();
            } while (--count >= 0);
        }
        g_memoryManager.Deallocate(allocation);
    }
    DAT_011f4464 = 0;
}