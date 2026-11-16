struct Vec_004e83e0 {
    float x, y, z;
    Vec_004e83e0 FUN_00439ef0(const Vec_004e83e0&) const;
    float FUN_00457990() const;
};
struct WaterActor_004e83e0 : PlayerCharacter {
    virtual void vfn_1f8();
virtual void vfn_1fc();
virtual void vfn_200();
virtual void vfn_204();
virtual void vfn_208();
virtual void vfn_20c();
virtual void vfn_210();
virtual void vfn_214();
virtual void vfn_218();
virtual void vfn_21c();
virtual void vfn_220();
virtual void vfn_224();
virtual void vfn_228();
    virtual bool IsExcludedFromWaterCheck(int);
};
struct RangeSetting_004e83e0 {
    float* FUN_00403e20();
};
extern RangeSetting_004e83e0 DAT_011c7b54;
struct WaterList_004e83e0 {
    void* FUN_00559450() const;
    void* FUN_007b52d0(void*) const;
    WaterActor_004e83e0*& FUN_006317a0(void*) const;
};
struct WaterScanner_004e83e0 {
    bool FUN_004e83e0(void* collection);
};
bool WaterScanner_004e83e0::FUN_004e83e0(void* collection)
{
    void* position;
    void* nextPosition = reinterpret_cast<WaterList_004e83e0*>(
        reinterpret_cast<char*>(collection) + 0x3c)->FUN_00559450();
    position = 0;
    while (nextPosition) {
    position = reinterpret_cast<WaterList_004e83e0*>(
                    reinterpret_cast<char*>(collection) + 0x3c)->FUN_007b52d0(nextPosition);
        if (nextPosition) {
            WaterActor_004e83e0* object = reinterpret_cast<WaterList_004e83e0*>(
                    reinterpret_cast<char*>(collection) + 0x3c)->FUN_006317a0(nextPosition);
            if (g_thePlayer == object)
                return true;
            else if (!object->IsExcludedFromWaterCheck(0)) {
                Vec_004e83e0 difference =
                    *reinterpret_cast<const Vec_004e83e0*>(&g_thePlayer->GetPos());
                Vec_004e83e0 distance =
                    *reinterpret_cast<const Vec_004e83e0*>(&object->GetPos());
                difference.z = 0.0f;
                distance.z = 0.0f;
                float playerPos = difference.FUN_00439ef0(distance).FUN_00457990();
                if (playerPos <= *DAT_011c7b54.FUN_00403e20())
                    return true;
            }
        }
        nextPosition = position;
    }
    return false;
}
