struct Vec3 {
    float x; float y; float z;
    Vec3() {}
    Vec3(float fx, float fy, float fz) { x = fx; y = fy; z = fz; }
    Vec3 operator*(float s) const { return Vec3(x * s, y * s, z * s); }
    Vec3& operator*=(float s) { x *= s; y *= s; z *= s; return *this; }
    Vec3& operator+=(const Vec3& p) { x += p.x; y += p.y; z += p.z; return *this; }
    void Unitize();
};
inline Vec3 operator*(float s, const Vec3& p) { Vec3 r; r.x = s * p.x; r.y = s * p.y; r.z = s * p.z; return r; }
struct NiMatrix3 {
    float m[3][3];
    Vec3 operator*(const Vec3& p) const {
        return Vec3(m[0][0] * p.x + m[0][1] * p.y + m[0][2] * p.z,
                    m[1][0] * p.x + m[1][1] * p.y + m[1][2] * p.z,
                    m[2][0] * p.x + m[2][1] * p.y + m[2][2] * p.z);
    }
};
struct NiTransform {
    NiMatrix3 m_Rotate;
    Vec3 m_Translate;
    float m_fScale;
    NiTransform operator*(const NiTransform& t) const;
    void InvertInto(NiTransform& out) const;
};
struct NiAVObjectStub {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28; int unk2C; int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44; int unk48; int unk4C; int unk50; int unk54; int unk58; int unk5C;
    int unk60; int unk64;
    NiTransform m_kWorld;
    NiTransform GetWorldTransform() const { return m_kWorld; }
};
struct NiParticleInfo {
    Vec3 m_kVelocity;
    int unk0C;
    int unk10;
    float m_fLastUpdate;
    int unk18;
};
struct NiPSysDataStub {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28; int unk2C; int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44; int unk48; int unk4C;
    unsigned short m_usActiveVertices;
    unsigned short unk52;
    int unk54; int unk58; int unk5C; int unk60; int unk64; int unk68; int unk6C;
    NiParticleInfo* m_pkParticleInfo;
};
struct GravityFieldStub {
    int unk00; int unk04; int unk08; int unk0C;
    NiAVObjectStub* m_pkTarget;
    int unk14;
    NiAVObjectStub* m_pkFieldObj;
    float m_fMagnitude;
    int unk20; int unk24; int unk28; int unk2C;
    Vec3 m_kDirection;
    void FUN_00c2aac0(float fTime, NiPSysDataStub* pkData);
};

void GravityFieldStub::FUN_00c2aac0(float fTime, NiPSysDataStub* pkData)
{
    NiTransform kField = m_pkFieldObj->m_kWorld;
    NiTransform kInv;
    {
        NiTransform kPSys = m_pkTarget->m_kWorld;
        kPSys.InvertInto(kInv);
    }
    Vec3 kAccel;
    {
        NiTransform kX = kInv * kField;
        Vec3 kDir = kX.m_Rotate * m_kDirection;
        kDir.Unitize();
        kDir *= m_fMagnitude;
        kAccel = kDir;
    }
    for (unsigned short i = 0; i < pkData->m_usActiveVertices; i++) {
        NiParticleInfo* pkInfo = &pkData->m_pkParticleInfo[i];
        float fDelta = fTime - pkInfo->m_fLastUpdate;
        if (fDelta != 0.0f)
            { Vec3 change = kAccel * fDelta; Vec3& velocity = pkInfo->m_kVelocity; velocity.x += change.x; float valueY = velocity.y; velocity.y = valueY + change.y; velocity.z += change.z; }
    }
}
