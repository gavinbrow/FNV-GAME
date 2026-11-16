struct BinaryStream {
    void* m_vtable;
    unsigned int m_position;
    void* m_owner;
    int (__cdecl *m_write)(BinaryStream*, const void*, unsigned int, unsigned int*, unsigned int);
    void Write(const void* data, unsigned int count) {
        unsigned int actualCount = count;
        m_position += m_write(this, data, count, &actualCount, 1);
    }
};
struct StreamContext {
    BinaryStream* OutputStream() {
        return *reinterpret_cast<BinaryStream**>(reinterpret_cast<unsigned char*>(this) + 0x250);
    }
};
struct FUN_00cc5730_class {
    void* m_vtable;
    unsigned char* m_objectData;
    void __thiscall FUN_00c8a280(StreamContext* context);
    void __thiscall FUN_00cc5730(StreamContext* context);
};
void __thiscall FUN_00cc5730_class::FUN_00cc5730(StreamContext* context) {
    FUN_00c8a280(context);
    unsigned char* data = m_objectData;
    context->OutputStream()->Write(data + 0x20, 0x40);
    context->OutputStream()->Write(data + 0x60, 0x40);
    context->OutputStream()->Write(data + 0xd0, 0x30);
    context->OutputStream()->Write(data + 0x100, 0x30);
    context->OutputStream()->Write(data + 0x140, 0x10);
    context->OutputStream()->Write(data + 0x150, 0x10);
    context->OutputStream()->Write(data + 0xa4, 4);
    context->OutputStream()->Write(data + 0xa8, 4);
    context->OutputStream()->Write(data + 0xb0, 4);
    context->OutputStream()->Write(data + 0xb4, 4);
}