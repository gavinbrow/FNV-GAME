void __cdecl FUN_00c908c0(VUC_Allocator* allocator, VUC_RealArray* array, int capacity, int stride);
struct VUC_BrakingStrategy { virtual void slot0(); virtual void slot1(); virtual void slot2(); virtual void calculate(float dt, VUC_Instance* vehicle, const VUC_Filtered& input, FUN_00e39400& output); };
void VUC_Instance::FUN_00e38a30(float dt, const VUC_Filtered& input, FUN_00e39400& output) throw()
{
    hkpVehicleInstance* vehicle = reinterpret_cast<hkpVehicleInstance*>(this);
    VUC_RealArray& fixed = output.m_isFixed;
    int count = vehicle->m_isFixed.m_size;
    VUC_Router* router = reinterpret_cast<VUC_Router*>(FUN_00c85750());
    VUC_Allocator* alloc = router->m_allocator;
    int capacity = fixed.m_capacityAndFlags & 0x3fffffff;
    if (capacity < count) {
        capacity *= 2;
        if (count >= capacity) capacity = count;
        FUN_00c908c0(alloc, &fixed, capacity, 1);
    }
    fixed.m_size = count;
    count = vehicle->m_isFixed.m_size;
    router = reinterpret_cast<VUC_Router*>(FUN_00c85750());
    alloc = router->m_allocator;
    capacity = output.m_brakingTorque.m_capacityAndFlags & 0x3fffffff;
    if (capacity < count) {
        capacity *= 2;
        if (count >= capacity) capacity = count;
        FUN_00c908c0(alloc, &output.m_brakingTorque, capacity, 4);
    }
    output.m_brakingTorque.m_size = count;
    for (int i=0; i<vehicle->m_isFixed.m_size; ++i) reinterpret_cast<char*>(fixed.m_data)[i] = vehicle->m_isFixed.m_data[i];
    output.m_unk18 = vehicle->m_wheelsTimeSinceMaxPedalInput;
    reinterpret_cast<VUC_BrakingStrategy*>(vehicle->m_brake)->calculate(dt, this, input, output);
    for (int i=0; i<output.m_isFixed.m_size; ++i) vehicle->m_isFixed.m_data[i] = reinterpret_cast<char*>(output.m_isFixed.m_data)[i];
    vehicle->m_wheelsTimeSinceMaxPedalInput = output.m_unk18;
}
