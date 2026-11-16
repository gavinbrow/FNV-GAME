extern "C" void* __cdecl FUN_00aa13e0(unsigned int size);
struct ParticleVector3 {
    float x, y, z;
};
struct ParticlePositionClone : FUN_00c63330 {
    unsigned int referenceCount;
    const char* name;
    unsigned int order;
    void* targetSystem;
    bool active;
    ParticleVector3 position;
    ParticleVector3 velocity;
    ParticleVector3 previousPosition;
    float lastUpdateTime;

    static __forceinline void* __cdecl operator new(unsigned int size) {
        return FUN_00aa13e0(size);
    }
};
struct FUN_00c637b0_Class : FUN_00c63840_Class {
    ParticlePositionClone* FUN_00c637b0(NiCloningProcess* process);
};
ParticlePositionClone* FUN_00c637b0_Class::FUN_00c637b0(NiCloningProcess* process)
{
    ParticlePositionClone* clone = new ParticlePositionClone();
    FUN_00c63840(reinterpret_cast<NiPSysModifier*>(clone), process);
    return clone;
}