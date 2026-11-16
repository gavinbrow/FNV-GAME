void* FUN_00c85750() throw();

struct VehicleStepInfo {
    float m_startTime;
    float m_endTime;
    float m_deltaTime;
    float m_invDeltaTime;
};
struct __declspec(align(16)) VehicleVector4 {
    float x, y, z, w;
};
struct VehicleData {
    void* m_vtable;
    unsigned short m_memSizeAndFlags;
    short m_referenceCount;
    VehicleVector4 m_gravity;
    signed char m_numWheels;
};
struct VehicleScratchAllocator {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void free(void* memory, unsigned int bytes);
};
struct VehicleMemoryRouter {
    char* m_stackTop;
    void* m_stackEnd;
    void* m_stackCapacity;
    void* m_heapFallback;
    VehicleScratchAllocator* m_allocator;
};
struct VehicleWheelCollide {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void collideWheels(float deltaTime, void* vehicle, void* scratch);
};
struct VehicleInstance {
    void* m_vtable;
    unsigned short m_memSizeAndFlags;
    short m_referenceCount;
    void* m_world;
    void* m_island;
    unsigned int m_userData;
    const char* m_name;
    void* m_entity;
    VehicleData* m_data;
    void* m_driverInput;
    void* m_steering;
    void* m_engine;
    void* m_transmission;
    void* m_brake;
    void* m_suspension;
    void* m_aerodynamics;
    VehicleWheelCollide* m_wheelCollide;
    void FUN_00e37940();
    void FUN_00e39030(const VehicleStepInfo* stepInfo, void* scratch);
    void FUN_00e39190(const VehicleStepInfo* stepInfo);
};

void VehicleInstance::FUN_00e39190(const VehicleStepInfo* stepInfo)
{
    FUN_00e37940();
    int wheelCount = m_data->m_numWheels;
    VehicleMemoryRouter* router = (VehicleMemoryRouter*)FUN_00c85750();
    char* originalTop = router->m_stackTop;
    float deltaTime = stepInfo->m_deltaTime;
    router->m_stackTop = originalTop + (((wheelCount * 3 << 5) + 127) & ~127);
    int capacityAndFlags = wheelCount | 0x80000000;

    m_wheelCollide->collideWheels(deltaTime, this, originalTop);
    FUN_00e39030(stepInfo, originalTop);
    ((VehicleMemoryRouter*)FUN_00c85750())->m_stackTop = originalTop;
    VehicleScratchAllocator* allocator =
        ((VehicleMemoryRouter*)FUN_00c85750())->m_allocator;
    if (!(capacityAndFlags & 0x80000000)) {
        allocator->free(originalTop, (capacityAndFlags & 0x3fffffff) * 3 << 5);
    }
}