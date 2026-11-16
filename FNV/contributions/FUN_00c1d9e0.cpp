#include <math.h>
extern int __cdecl FUN_00ecadb8(void);
struct C1d9e0_Emitter : MeshEmitter_c1cf50 {
    bool __thiscall FUN_00c1d9e0(NiGeometry* pkGeometry, NiPoint3& kPosition, NiPoint3& kVelocity);
};
bool __thiscall C1d9e0_Emitter::FUN_00c1d9e0(NiGeometry* pkGeometry, NiPoint3& kPosition, NiPoint3& kVelocity)
{
    int randomValue = FUN_00ecadb8();
    char* data = *(char**)((char*)pkGeometry + 0xb8);
    unsigned short count = *(unsigned short*)(data + 8);
    randomValue %= count;
    NiPoint3* positions = *(NiPoint3**)(data + 0x20);
    NiPoint3b* normals = *(NiPoint3b**)(data + 0x24);
    if (positions == 0)
        return false;
    kPosition = positions[randomValue];
    NiPoint3b normal = normals[randomValue];
    if (velocityMode == 0 && *(NiPoint3b**)(*(char**)((char*)pkGeometry + 0xb8) + 0x24) != 0)
    {
        float length = (float)sqrt(kVelocity.x*kVelocity.x + kVelocity.y*kVelocity.y + kVelocity.z*kVelocity.z);
        NiPoint3b result = normal * length;
        kVelocity = *(NiPoint3*)&result;
    }
    FUN_00c1cf50((NiAVObject*)pkGeometry, (NiPoint3b&)kPosition, (NiPoint3b&)kVelocity);
    return true;
}