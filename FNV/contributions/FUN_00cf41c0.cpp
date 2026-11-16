extern "C" void __cdecl FUN_00d86100(void* view, void* object);

struct BinaryStream {
    void* vtable;
    unsigned int absolutePosition;
    unsigned int (__cdecl *read)(BinaryStream*, void*, unsigned int, unsigned int*, unsigned int);

    template <typename T> void Load(T* dest) {
        unsigned int byteCount = sizeof(T);
        absolutePosition += read(this, dest, sizeof(T), &byteCount, 1);
    }
};
struct StreamView {
    BinaryStream* stream() {
        return *reinterpret_cast<BinaryStream**>(reinterpret_cast<char*>(this) + 0x24c);
    }
};
struct SerializedRecord {
    unsigned int unk00, unk04, unk08, unk0c, unk10;
    unsigned int m_14, m_18, m_1c, m_20;
    void FUN_00cf41c0(StreamView* view);
};
void SerializedRecord::FUN_00cf41c0(StreamView* view) {
    FUN_00d86100(view, this);
    view->stream()->Load(&m_14);
    view->stream()->Load(&m_18);
    view->stream()->Load(&m_1c);
    view->stream()->Load(&m_20);
}