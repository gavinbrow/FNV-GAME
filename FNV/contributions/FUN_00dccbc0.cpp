struct MeshShapeTriangle {
    void* vtable;
    int unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    hkVector4 vertex0, vertex1, vertex2;
};
struct __declspec(align(16)) MeshShapeBuffer {
    hkVector4 storage[32];
};
struct MeshShapeVTable {
    virtual void vf00();
    virtual void vf04();
    virtual void vf08();
    virtual int vf0c(unsigned int key);
    virtual void vf10();
    virtual MeshShapeTriangle* vf14(unsigned int key, MeshShapeBuffer* storage);
};
extern float DAT_011b2e90;
extern "C" hkBool* __cdecl FUN_00ceb8d0(hkBool* result, const hkVector4* v0,
                                     const hkVector4* v1, const hkVector4* v2, float tolerance);
struct MeshShapeDCCBC0 : public hkpMeshShape {
    int FUN_00dccbc0();
};
int MeshShapeDCCBC0::FUN_00dccbc0() {
    if (*reinterpret_cast<unsigned int*>(&m_scaling.z) == 0)
        return -1;
    MeshShapeBuffer buffer;
    MeshShapeTriangle* triangle =
        ((MeshShapeVTable*)this)->vf14(0, &buffer);
    hkBool result;
    if (!*FUN_00ceb8d0(&result, &triangle->vertex0, &triangle->vertex1,
                        &triangle->vertex2, DAT_011b2e90))
        return 0;
    return ((MeshShapeVTable*)this)->vf0c(0);
}