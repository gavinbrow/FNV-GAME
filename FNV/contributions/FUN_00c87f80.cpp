struct NiStream {
    int unk00;
    unsigned int version;
};
struct NiCollisionObject {
    void LinkObject(NiStream&);
};
struct LegacyLinker : NiCollisionObject {
    void FUN_00c6bb70(NiStream*);
    void FUN_00c87f80(NiStream*);
};
void LegacyLinker::FUN_00c87f80(NiStream* stream) {
    if (stream->version >= 0x15)
        FUN_00c6bb70(stream);
    else
        NiCollisionObject::LinkObject(*stream);
}
