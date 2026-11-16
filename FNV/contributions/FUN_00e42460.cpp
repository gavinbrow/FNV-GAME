union __declspec(intrin_type) __declspec(align(16)) __m128 { float m128_f32[4]; unsigned __int64 m128_u64[2]; };

struct S00e42460_Vec4 {
    __m128 m_quad;
};

class hkpCollidable;

class hkpCollidableCollidableFilter { public: virtual ~hkpCollidableCollidableFilter(); };
class hkpShapeCollectionFilter { public: virtual ~hkpShapeCollectionFilter(); };
class hkpRayShapeCollectionFilter { public: virtual ~hkpRayShapeCollectionFilter(); };
class hkpRayCollidableFilter { public: virtual ~hkpRayCollidableFilter(); };

class hkpCollisionFilter : public hkReferencedObject, public hkpCollidableCollidableFilter, public hkpShapeCollectionFilter,
                           public hkpRayShapeCollectionFilter, public hkpRayCollidableFilter {
public:
    hkUint32 m_prepad0;
    hkUint32 m_prepad1;
    hkUint32 m_type;
};

class hkpAabbPhantom : public hkReferencedObject {
public:
    virtual void v04(); virtual void v08(); virtual void v0c(); virtual void v10();
    virtual void v14(); virtual void v18(); virtual void v1c(); virtual void v20();
    virtual void v24();
    virtual void ensureDeterministicOrder();

    int unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    int unk40, unk44, unk48, unk4c, unk50, unk54, unk58, unk5c, unk60, unk64, unk68, unk6c, unk70, unk74, unk78, unk7c;
    int unk80, unk84, unk88, unk8c, unk90, unk94, unk98, unk9c, unka0, unka4, unka8, unkac, unkb0, unkb4, unkb8, unkbc;
    int unkc0, unkc4, unkc8, unkcc;
    hkArray<hkpCollidable*> m_overlappingCollidables;
};

struct S00e42460_VehicleData {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    hkInt8 m_numWheels;
};

struct S00e42460_WheelInfo {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    int unk40, unk44, unk48, unk4c;
    S00e42460_Vec4 m_hardPointWs;
    S00e42460_Vec4 m_rayEndPointWs;
    int unk70, unk74, unk78, unk7c, unk80, unk84, unk88, unk8c;
    int unk90, unk94, unk98, unk9c, unka0, unka4, unka8, unkac;
    int unkb0, unkb4, unkb8, unkbc, unkc0, unkc4, unkc8, unkcc;
    int unkd0, unkd4, unkd8, unkdc;
};

struct S00e42460_VehicleInstance {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18;
    S00e42460_VehicleData* m_data;
    int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c, unk40, unk44;
    hkArray<S00e42460_WheelInfo> m_wheelsInfo;
};

struct S00e42460_RayInput {
    S00e42460_Vec4 m_from;
    S00e42460_Vec4 m_to;
    hkUint32 m_filterInfo;
    const hkpRayShapeCollectionFilter* m_rayShapeCollectionFilter;
    hkUlong m_userData;
    int unk2c;
};

struct S00e42460_WorldRayCastOutput {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    int unk40, unk44, unk48, unk4c, unk50, unk54, unk58, unk5c;
};

struct S00e42460_RayCastCommand {
    S00e42460_RayInput m_rayInput;
    hkUint32 m_filterType;
    hkInt32 m_filterSize;
    hkpCollidable* const* m_collidables;
    int m_numCollidables;
    S00e42460_WorldRayCastOutput* m_results;
    int m_resultsCapacity;
    int m_numResultsOut;
    hkBool m_useCollector;
};

class S00e42460_RayCastWheelCollide : public hkpVehicleRayCastWheelCollide {
public:
    int FUN_00e42460(const S00e42460_VehicleInstance* vehicle, const hkpCollisionFilter* collisionFilter, hkInt32 filterSize,
                     S00e42460_RayCastCommand* commandStorage, S00e42460_WorldRayCastOutput* outputStorage) const;
};

int S00e42460_RayCastWheelCollide::FUN_00e42460(const S00e42460_VehicleInstance* vehicle, const hkpCollisionFilter* collisionFilter, hkInt32 filterSize,
                                                S00e42460_RayCastCommand* commandStorage, S00e42460_WorldRayCastOutput* outputStorage) const
{
    m_phantom->ensureDeterministicOrder();

    const int numCollidables = m_phantom->m_overlappingCollidables.m_size;
    if (numCollidables > 0)
    {
        const hkInt8 numWheels = vehicle->m_data->m_numWheels;
        if (numWheels > 0)
        {
            int i = 0;
            int count = (hkUint8)numWheels;
            do
            {
                S00e42460_RayCastCommand& command = *commandStorage;
                const S00e42460_WheelInfo& wheelInfo = vehicle->m_wheelsInfo.m_data[i];

                command.m_rayInput.m_from.m_quad = wheelInfo.m_hardPointWs.m_quad;
                command.m_rayInput.m_to.m_quad = wheelInfo.m_rayEndPointWs.m_quad;
                command.m_rayInput.m_filterInfo = m_wheelCollisionFilterInfo;
                command.m_rayInput.m_rayShapeCollectionFilter = collisionFilter;
                command.m_filterType = collisionFilter->m_type;
                command.m_filterSize = filterSize;
                command.m_useCollector = false;
                command.m_collidables = m_phantom->m_overlappingCollidables.m_data;
                command.m_results = outputStorage;
                command.m_numCollidables = numCollidables;
                command.m_resultsCapacity = 1;
                command.m_numResultsOut = 0;
                ++i;
                ++commandStorage;
                ++outputStorage;
            } while (--count != 0);
        }
        return numWheels;
    }
    return 0;
}
