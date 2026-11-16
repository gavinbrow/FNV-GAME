
struct BinaryStream {
    void* unk00;
    unsigned int offset;
    void* unk08;
    unsigned int (__cdecl *write)(BinaryStream*, const void*, unsigned int, unsigned int*, unsigned int);
    __forceinline unsigned int WriteData(const void* data, unsigned int size) {
        unsigned int elementSize = 4;
        return write(this,data,size,&elementSize,1);
    }
};
struct StreamSlot { BinaryStream* stream; };
class NiStream {
public:
    virtual void v00(); virtual void v01(); virtual void v02();
    virtual void v03(); virtual void v04(); virtual void v05();
    virtual void v06(); virtual void v07(); virtual void v08();
    virtual void v09(); virtual void v10(); virtual void v11();
    virtual void RegisterObject(NiAVObject*);
    BinaryStream* GetBinaryStream() {
        return reinterpret_cast<StreamSlot*>(reinterpret_cast<unsigned char*>(this) + 0x250)->stream;
    }
};
class MeshUpdateStreamWriter : public NiPSysMeshUpdateModifier {
public:
    void FUN_00c31950(NiStream*);
    void FUN_00c211c0(NiStream*);
};
void MeshUpdateStreamWriter::FUN_00c211c0(NiStream* stream) {
    FUN_00c31950(stream);
    unsigned int meshCount = m_usNumMeshes;
    BinaryStream* binary = stream->GetBinaryStream();
    binary->offset += binary->WriteData(&meshCount, 4);
    for (unsigned int i = 0; i < meshCount; ++i)
        stream->RegisterObject(m_ppkMeshes[i]);
}
