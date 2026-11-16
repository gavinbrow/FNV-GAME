struct InputBinaryStream2 {
    unsigned int streamFlags;
    unsigned int bytesRead;
    unsigned int readMode;
    unsigned int (__cdecl *readData)(InputBinaryStream2*, void*, unsigned int, unsigned int*, unsigned int);
    void ReadFloat(float& value) {
        unsigned int bytes = 4;
        bytesRead += readData(this, &value, 4, &bytes, 1);
    }
};
struct StreamView {
    virtual void slot00() = 0;
    virtual void slot01() = 0;
    virtual void slot02() = 0;
    virtual void slot03() = 0;
    virtual void slot04() = 0;
    virtual void slot05() = 0;
    virtual void slot06() = 0;
    virtual void slot07() = 0;
    virtual void slot08() = 0;
    virtual void slot09() = 0;
    virtual void slot10() = 0;
    virtual void slot11() = 0;
    virtual void ReadObject(unsigned int) = 0;
    InputBinaryStream2* Input() {
        return *reinterpret_cast<InputBinaryStream2**>(reinterpret_cast<char*>(this) + 0x250);
    }
};
struct SphericalColliderReader : NiPSysCollider {
    unsigned int& linkId() {
        return *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x2c);
    }
    float& radius() {
        return *reinterpret_cast<float*>(reinterpret_cast<char*>(this) + 0x30);
    }
    void FUN_00c32900(NiStream& stream);
    void FUN_00c280c0(NiStream& stream);
};
void SphericalColliderReader::FUN_00c280c0(NiStream& stream)
{
    FUN_00c32900(stream);
    StreamView& reader = reinterpret_cast<StreamView&>(stream);
    reader.ReadObject(linkId());
    reader.Input()->ReadFloat(radius());
}