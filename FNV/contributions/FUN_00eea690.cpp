extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long* value);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long* value);
extern const char* _EmptyFS;

struct FixedStringHolder {
    void* m_vftable;
    unsigned int m_uiUnknown1;
    unsigned int m_uiUnknown2;
    unsigned int m_uiUnknown3;
    const char* m_pString;

    void FUN_00eea690(const char** source);
};

void FixedStringHolder::FUN_00eea690(const char** source) {
    const char* newString = *source;
    if (m_pString != newString) {
        if (newString != _EmptyFS) {
            InterlockedIncrement(reinterpret_cast<volatile long*>(const_cast<char*>(newString) - 8));
        }
        if (m_pString != _EmptyFS) {
            InterlockedDecrement(reinterpret_cast<volatile long*>(const_cast<char*>(m_pString) - 8));
        }
        m_pString = newString;
    }
}