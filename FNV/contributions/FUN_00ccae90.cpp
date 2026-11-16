struct FUN_00ccae90_Object {
    unsigned int m_type;
    unsigned int m_referenceCount;
    unsigned int m_flags;
    void* m_resource;
    void __thiscall FUN_00ccae90(char release);
};
struct ResourceManager {
    void __thiscall FUN_00aa4060(void* resource);
};
extern ResourceManager DAT_011f6238;
extern __declspec(thread) unsigned int tlsCurrentContext;
void FUN_00ccae90_Object::FUN_00ccae90(char release) {
    unsigned int previousContext = tlsCurrentContext;
    tlsCurrentContext = 0x10;
    if (release) {
        DAT_011f6238.FUN_00aa4060(m_resource);
        m_resource = 0;
    }
    tlsCurrentContext = previousContext;
}