struct EffectObject : NiDynamicEffect {
    void __thiscall FUN_00a5a900(NiStream* stream);
    void __thiscall FUN_00a68f80(NiStream* stream);
};
static __forceinline unsigned int WriteBytes(NiBinaryStream* output, const void* bytes, unsigned int length) {
    unsigned int componentLength = length;
    unsigned int written = output->m_pfnWrite(output, bytes, length, &componentLength, 1);
    output->m_uiAbsoluteCurrentPos += written;
    return written;
}
typedef void (__thiscall *SaveLinkedObject)(NiStream*, NiNode*);
static __forceinline void WriteLinkedObject(NiStream* stream, NiNode*& object) {
    ((SaveLinkedObject*)stream->m_vtable)[12](stream, object);
}
void __thiscall EffectObject::FUN_00a68f80(NiStream* stream) {
    FUN_00a5a900(stream);
    unsigned char enabled = m_bOn;
    NiBinaryStream* output = stream->m_pkOstr;
    WriteBytes(output, &enabled, 1);
    int objectCount = m_kUnaffectedNodeList.m_kAllocator.m_uiCount;
    output = stream->m_pkOstr;
    WriteBytes(output, &objectCount, 4);
    if (objectCount > 0) {
        NiTListItem<NiNode*>* node = m_kUnaffectedNodeList.m_pkTail;
        while (node) {
NiNode*& element = node->m_element;
            node = node->m_pkPrev;
            WriteLinkedObject(stream, element);
        }
    }
}