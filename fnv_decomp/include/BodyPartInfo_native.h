#ifndef FNV_EXPERIMENT_BODYPARTINFO_H
#define FNV_EXPERIMENT_BODYPARTINFO_H
#include "NiPoint3.h"
class BGSDebris;
class BGSExplosion;
class BGSImpactDataSet;
#pragma pack(push, 4)
class BodyPartInfo
{
  public:
    BodyPartInfo();
    void SwapEndianFields();
    void Initialize();
    float m_fDamageMultiplier;              // +0x0, 4 bytes
    unsigned char cFlags;                   // +0x4, 1 bytes
    unsigned char cType;                    // +0x5, 1 bytes
    unsigned char m_ucPartID;               // +0x6, 1 bytes
    char m_cActorValue;                     // +0x7, 1 bytes
    unsigned char m_ucHealthPercent;        // +0x8, 1 bytes
    unsigned char m_ucHitChance;            // +0x9, 1 bytes
    unsigned char m_ucLimbReplacementType;  // +0xA, 1 bytes
    unsigned char layoutPaddingB[1];
    BGSDebris* m_pExplosion;        // +0xC, 4 bytes
    BGSExplosion* m_pDebrisObject;  // +0x10, 4 bytes
    float m_fExplosionChance;       // +0x14, 4 bytes
    float m_fDebrisScale;           // +0x18, 4 bytes
    unsigned char m_ucSeverable;    // +0x1C, 1 bytes
    unsigned char layoutPadding1D[3];
    BGSDebris* m_pRelatedObject1;         // +0x20, 4 bytes
    BGSExplosion* m_pRelatedObject2;      // +0x24, 4 bytes
    float m_fValue3;                      // +0x28, 4 bytes
    NiPoint3 m_kPoint1;                   // +0x2C, 12 bytes
    NiPoint3 m_kPoint2;                   // +0x38, 12 bytes
    BGSImpactDataSet* m_pRelatedObject3;  // +0x44, 4 bytes
    BGSImpactDataSet* m_pRelatedObject4;  // +0x48, 4 bytes
    unsigned char m_ucByte1;              // +0x4C, 1 bytes
    unsigned char m_ucByte2;              // +0x4D, 1 bytes
    unsigned char layoutPadding4E[2];
    float m_fValue4;  // +0x50, 4 bytes
    // void __cdecl BodyPartInfo::*()
    // void __cdecl BodyPartInfo::*()
    // void __cdecl BodyPartInfo::*()
};
#pragma pack(pop)
FNV_STATIC_ASSERT(sizeof(BodyPartInfo) == 84);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_fDamageMultiplier) == 0);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, cFlags) == 4);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, cType) == 5);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_ucPartID) == 6);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_cActorValue) == 7);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_ucHealthPercent) == 8);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_ucHitChance) == 9);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_ucLimbReplacementType) == 10);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_pExplosion) == 12);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_pDebrisObject) == 16);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_fExplosionChance) == 20);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_fDebrisScale) == 24);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_ucSeverable) == 28);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_pRelatedObject1) == 32);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_pRelatedObject2) == 36);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_fValue3) == 40);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_kPoint1) == 44);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_kPoint2) == 56);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_pRelatedObject3) == 68);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_pRelatedObject4) == 72);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_ucByte1) == 76);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_ucByte2) == 77);
FNV_STATIC_ASSERT(offsetof(BodyPartInfo, m_fValue4) == 80);
#endif
