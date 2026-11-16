#include "h_17f0267c5f44.h"

// Stand-ins for the classes the pack header only forward-declares.
// Field offsets follow the offsets used by FUN_00c32490's machine code.

class NiPSysData : public NiObject
{
public:
    // NiObject supplies virtual slots 0..24 (vtable 0x00..0x64).
    virtual void vf25();
    virtual void vf26();
    virtual void vf27();
    virtual void vf28();
    virtual void vf29();
    virtual void vf30();
    virtual void vf31();
    virtual void vf32();
    virtual void vf33();
    virtual void vf34();
    virtual void vf35();
    virtual void vf36();
    virtual void vf37();
    virtual void vf38();
    virtual void RemoveParticle(unsigned int uiIndex); // slot 41 -> +0xA4

    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    NiPoint3* m_pkVertex; // +0x20: per-particle positions
};

class NiPSysSpawnModifier : public NiObject
{
public:
    // NiObject supplies virtual slots 0..24.
    virtual void vf25();
    virtual void vf26();
    virtual void vf27();
    virtual void vf28();
    virtual void vf29();
    virtual void vf30();
    virtual void vf31();
    virtual void vf32();
    virtual void vf33();
    virtual void vf34();
    virtual void vf35();
    virtual void vf36();
    virtual void vf37();
    virtual void vf38();
    virtual void SpawnParticles(float fTime, float fCollisionTime,
        unsigned int uiIndex, NiPSysData* pkData); // slot 41 -> +0xA4
};

class NiPSysColliderManager : public NiObject
{
public:
    int unk08;
    int unk0C;
    NiPSysData* m_pkData; // +0x10
};

struct FUN_00c32490_shell : public NiPSysCollider
{
    void FUN_00c32490(float fTime, NiPSysData* pkData, unsigned int uiIndex);
};

void FUN_00c32490_shell::FUN_00c32490(float fTime, NiPSysData* pkData,
    unsigned int uiIndex)
{
    pkData->m_pkVertex[(unsigned short)uiIndex] = m_kCollisionPoint;

    if (m_bSpawnOnCollide && m_pkSpawnModifier)
    {
        m_pkSpawnModifier->SpawnParticles(fTime, m_fCollisionTime, uiIndex,
            m_pkManager->m_pkData);
    }

    if (m_bDieOnCollide)
    {
        pkData->RemoveParticle(uiIndex);
    }
}
