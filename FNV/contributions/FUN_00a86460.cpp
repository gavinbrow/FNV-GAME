class NiStream;
struct SkinGraph {
    void* vtable;
    unsigned int refCount;
    NiObject* skinData;
    NiObject* skinPartition;
    NiObject* rootParent;
    NiObject** bones;
    bool FUN_00a5d2f0(NiStream&);
    bool FUN_00a86460(NiStream& stream);
};
typedef void (__thiscall *VisitStreamable)(NiObject*, NiStream&);
__forceinline void VisitLinkedObject(NiObject* object, NiStream& stream) {
    void** methods = *reinterpret_cast<void***>(object);
    reinterpret_cast<VisitStreamable>(methods[21])(object, stream);
}
bool SkinGraph::FUN_00a86460(NiStream& stream) {
    if (!FUN_00a5d2f0(stream)) return false;
    VisitLinkedObject(skinData, stream);
    if (skinPartition) VisitLinkedObject(skinPartition, stream);
    VisitLinkedObject(rootParent, stream);
    unsigned int count = *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(skinData) + 0x44);
    for (unsigned int index=0; index < count; ++index) {
        VisitLinkedObject(bones[index], stream);
    }
    return true;
}