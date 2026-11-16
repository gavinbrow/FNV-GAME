
struct OutputBinaryStream : NiBinaryStream {
    __forceinline void WriteBuffer(
        const void* data, unsigned int bytes,
        unsigned int* componentSizes, unsigned int componentCount)
    {
        unsigned int written = m_pfnWrite(
            this, data, bytes, componentSizes, componentCount);
        m_uiAbsoluteCurrentPos += written;
    }
};
struct OutputStream : NiStream {
    OutputBinaryStream* m_pkOstr;
    void FUN_00a641f0(NiFixedString&);
};
struct LinkOutput {
    virtual void Slot00(); virtual void Slot04(); virtual void Slot08();
    virtual void Slot0c(); virtual void Slot10(); virtual void Slot14();
    virtual void Slot18(); virtual void Slot1c(); virtual void Slot20();
    virtual void Slot24(); virtual void Slot28(); virtual void Slot2c();
    virtual void SaveObject(NiParticleSystem*);
};
struct BinaryObjectBase {
    void* vtable;
    unsigned int referenceCount;
    void FUN_00a89af0(OutputStream&);
};
struct ParticleModifierBinary : BinaryObjectBase {
    NiFixedString name;
    unsigned int order;
    NiParticleSystem* target;
    bool active;
    void FUN_00c31950(OutputStream&);
};
template<class T>
__forceinline void PrimitiveWrite(OutputBinaryStream* stream, const T& value)
{
    unsigned int size = sizeof(T);
    stream->WriteBuffer(&value, sizeof(T), &size, 1);
}
__forceinline void BooleanWrite(OutputBinaryStream* stream, bool value)
{
    unsigned int size = 1;
    stream->WriteBuffer(&value, 1, &size, 1);
}
void ParticleModifierBinary::FUN_00c31950(OutputStream& stream)
{
    FUN_00a89af0(stream);
    stream.FUN_00a641f0(name);
    PrimitiveWrite(stream.m_pkOstr, order);
    reinterpret_cast<LinkOutput*>(&stream)->SaveObject(target);
    BooleanWrite(stream.m_pkOstr, active);
}
