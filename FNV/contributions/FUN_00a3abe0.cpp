struct NiPoint3 {
    float x;
    float y;
    float z;
};

extern const NiPoint3 DAT_011f426c;

struct NiBound {
    NiPoint3 center;
    float radius;
    void FUN_00a7ee30(unsigned int vertexCount, const NiPoint3* vertices);
    void FUN_00a7f3f0(const NiBound* other);
};

struct MorphTarget {
    NiPoint3* vertices;
    void* name;
    float weight;
    void* interpolator;
};

struct MorphData {
    void* vtable;
    unsigned int refCount;
    unsigned int targetCount;
    unsigned int vertexCount;
    MorphTarget* targets;
    MorphTarget* GetTarget(unsigned int index) const {
        return index < targetCount ? &targets[index] : 0;
    }
};

struct GeometryData {
    NiBound* GetBound() {
        return reinterpret_cast<NiBound*>(reinterpret_cast<char*>(this) + 0x10);
    }
};

struct Geometry {
    GeometryData* GetModelData() const {
        return *reinterpret_cast<GeometryData* const*>(
            reinterpret_cast<const char*>(this) + 0xb8);
    }
};

struct MorpherController {
    MorphData* GetMorphData() const {
        return *reinterpret_cast<MorphData* const*>(
            reinterpret_cast<const char*>(this) + 0x38);
    }
    Geometry* GetGeometry() const {
        return *reinterpret_cast<Geometry* const*>(
            reinterpret_cast<const char*>(this) + 0x2c);
    }
    void FUN_00a3abe0();
};

void MorpherController::FUN_00a3abe0() {
    NiBound bounds;
    const unsigned int count = GetMorphData()->targetCount;
    if (count != 0) {
        MorphData* data = GetMorphData();
        bounds.FUN_00a7ee30(data->vertexCount, data->GetTarget(0)->vertices);
        for (unsigned int i = 1; i < count; ++i) {
            NiBound nextBounds;
            data = GetMorphData();
            nextBounds.FUN_00a7ee30(data->vertexCount, data->GetTarget(i)->vertices);
            bounds.FUN_00a7f3f0(&nextBounds);
        }
    } else {
        bounds.center = DAT_011f426c;
        bounds.radius = 0.0f;
    }
    volatile float radiusValue = bounds.radius;
    NiBound* destination = GetGeometry()->GetModelData()->GetBound();
    destination->center = bounds.center;
    destination->radius = radiusValue;
}