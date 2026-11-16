#include <math.h>
struct MeshPoint { float x,y,z; MeshPoint() {} MeshPoint(float a,float b,float c): x(a),y(b),z(c) {} MeshPoint operator+(const MeshPoint& r) const { return MeshPoint(x+r.x,y+r.y,z+r.z); } MeshPoint operator-(const MeshPoint& r) const { return MeshPoint(x-r.x,y-r.y,z-r.z); } MeshPoint operator*(float r) const { return MeshPoint(x*r,y*r,z*r); } };
inline MeshPoint operator*(float l,const MeshPoint& r) { return MeshPoint(l*r.x,l*r.y,l*r.z); }
struct GeometryDataLayout {
    void* vtable;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    MeshPoint* vertices;
    MeshPoint* normals;
};
struct GeometryLayout {
    void** vtable;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int unk94;
    int unk98;
    int unk9c;
    int unka0;
    int unka4;
    int unka8;
    int unkac;
    int unkb0;
    int unkb4;
    GeometryDataLayout* modelData;
};
struct EmitterLayout {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int velocityType;
    int emissionType;
};
struct GeometryRuntimeType { const char* name; const GeometryRuntimeType* parent; };
extern GeometryRuntimeType DAT_011f4a48;
extern const double DAT_01099ee0;
extern "C" void __cdecl FUN_00525340(MeshPoint* point);
typedef int (__thiscall *GeometryTestFn)(NiGeometry*);
typedef GeometryRuntimeType* (__thiscall *GeometryRTTIFn)(NiGeometry*);
typedef unsigned short (__thiscall *GetTriangleCountFn)(void*);
typedef void (__thiscall *GetTriangleIndicesFn)(void*, unsigned int, unsigned short*, unsigned short*, unsigned short*);
struct MeshEmitterCandidate : FUN_00c1f5f0_shell {
    bool __thiscall FUN_00c1eb20(NiGeometry* geometry, MeshPoint& position, MeshPoint& velocity);
    bool __thiscall FUN_00c1dae0(NiGeometry* geometry, MeshPoint& position, MeshPoint& velocity);
    void __thiscall FUN_00c1cf50(NiGeometry* geometry, MeshPoint& position, MeshPoint& velocity);
};
bool MeshEmitterCandidate::FUN_00c1eb20(NiGeometry* geometry, MeshPoint& position, MeshPoint& velocity) {
    if (geometry) {
    if ((reinterpret_cast<GeometryTestFn>((reinterpret_cast<GeometryLayout*>(geometry)->vtable)[7]))(geometry)) {
        unsigned int triangleCount = (reinterpret_cast<GetTriangleCountFn>((reinterpret_cast<void**>(reinterpret_cast<GeometryLayout*>(geometry)->modelData->vtable))[42]))((reinterpret_cast<GeometryLayout*>(geometry)->modelData));
        unsigned int triangleIndex = static_cast<unsigned int>(NiRand()) % triangleCount;
        if (triangleIndex == triangleCount)
            triangleIndex = triangleCount - 1;
        unsigned short vertex0, vertex1, vertex2;
        int triangleAttempts = 0;
        do {
            (reinterpret_cast<GetTriangleIndicesFn>((reinterpret_cast<void**>(reinterpret_cast<GeometryLayout*>(geometry)->modelData->vtable))[43]))((reinterpret_cast<GeometryLayout*>(geometry)->modelData), triangleIndex, &vertex0, &vertex1, &vertex2);
            if (vertex0 != vertex1 && vertex0 != vertex2 && vertex1 != vertex2)
                break;
            triangleIndex += 1;
            if (triangleIndex >= triangleCount)
                triangleIndex = 0;
            triangleAttempts += 1;
        } while (triangleAttempts < 6);
        const MeshPoint* vertices = reinterpret_cast<GeometryLayout*>(geometry)->modelData->vertices;
        const MeshPoint* __restrict normals;
        normals = reinterpret_cast<GeometryLayout*>(geometry)->modelData->normals;
        if (!vertices)
            return false;
        MeshPoint v0 = vertices[vertex0];
        MeshPoint v1 = vertices[vertex1];
        MeshPoint v2 = vertices[vertex2];
        const float oneThird = 1.0f / 3.0f;
        MeshPoint vertexSum = v0 + v1 + v2;
        position = vertexSum * oneThird;
        if (reinterpret_cast<EmitterLayout*>(this)->velocityType == 0 && normals) {
            MeshPoint normal0 = normals[vertex0];
            MeshPoint normal1 = normals[vertex1];
            MeshPoint normal2 = normals[vertex2];
            MeshPoint normalSum = normal0 + normal1 + normal2;
            MeshPoint normal = normalSum * oneThird;
            FUN_00525340(&normal);
            float magnitude = sqrtf(velocity.x * velocity.x + velocity.y * velocity.y + velocity.z * velocity.z);
            velocity = normal * magnitude;
        }
        if (reinterpret_cast<EmitterLayout*>(this)->emissionType == 3) {
            MeshPoint edgeA = v1 - v0;
            MeshPoint edgeB = v2 - v0;
            float scaleA = FUN_00c1ced0(static_cast<float>(NiRand()) / DAT_01029790);
            float scaleB = static_cast<float>(NiRand()) / DAT_01029790;
            position = edgeA + (scaleA * (edgeB * scaleB - edgeA) + v0);
        }
        FUN_00c1cf50(geometry, position, velocity);
        return true;
    }
    GeometryRuntimeType* runtimeType = reinterpret_cast<GeometryRTTIFn>((reinterpret_cast<GeometryLayout*>(geometry)->vtable)[2])(geometry);
    for (; runtimeType; runtimeType = const_cast<GeometryRuntimeType*>(runtimeType->parent)) {
        if (runtimeType == &DAT_011f4a48)
            return FUN_00c1dae0(geometry, position, velocity);
    }
    }
    return false;
}
