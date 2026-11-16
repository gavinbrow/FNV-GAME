struct FNVBinaryInput {
    void* m_vtable;
    unsigned int m_uiCurrentPos;
    unsigned int m_uiUnknown08;
    unsigned int (__cdecl* m_pfnRead)(FNVBinaryInput*, void*, unsigned int, unsigned int*, unsigned int);

    void Read(void* buffer, unsigned int size) {
        m_uiCurrentPos += m_pfnRead(this, buffer, size, &size, 1);
    }
};

struct FNVStream {
    void FUN_00a641f0(NiFixedString& value);

    FNVBinaryInput* GetInput() const {
        return *reinterpret_cast<FNVBinaryInput* const*>(reinterpret_cast<const char*>(this) + 0x250);
    }
};

struct NiTextKeyFnv {
    float m_fTime;
    NiFixedString m_kText;

    void FUN_00a57930(FNVStream& stream);
};

void NiTextKeyFnv::FUN_00a57930(FNVStream& stream)
{
    stream.GetInput()->Read(&m_fTime, sizeof(m_fTime));
    stream.FUN_00a641f0(m_kText);
}
