extern const double DAT_0101db88;
extern const float DAT_0101e704;
extern const float DAT_0101e340;

struct NiPoint3 {
    float x, y, z;
    NiPoint3 operator-(const NiPoint3& other) const;
};

extern "C" int FUN_004b5470(NiPoint3* point, float value);

struct ProjectileImpactCandidate : ProjectileImpact {
    bool FUN_00935820(const NiPoint3& point, float value, bool adjust, int unused_stack);
};

bool ProjectileImpactCandidate::FUN_00935820(const NiPoint3& point, float value, bool adjust, int unused_stack)
{
    float upper;
    float lower;
    float upperBase;
    {
        NiPoint3 origin = reinterpret_cast<NiPoint3&>(this->position());
        NiPoint3 result = origin - point;

        upper = DAT_0101e704;
        lower = origin.z - DAT_0101db88;
        upperBase = origin.z + upper + DAT_0101db88;
        if (point.z > lower && point.z < upperBase) {
            result.z = 0.0f;
        }
        if (adjust) {
            float adjustment = DAT_0101e340;
            value += adjustment;
        }
        return FUN_004b5470(&result, value) <= 0;
    }
}

