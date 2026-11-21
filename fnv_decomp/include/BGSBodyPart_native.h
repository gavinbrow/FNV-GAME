#ifndef FNV_EXPERIMENT_BGSBODYPART_H
#define FNV_EXPERIMENT_BGSBODYPART_H
#include "TESModelPSA_native.h"
#include "BodyPartInfo_native.h"
class TESForm;
class TESFile;
class QueuedFile;
enum IO_TASK_PRIORITY
{
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_CRITICAL = 0,
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_VERY_HIGH = 1,
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_HIGH = 2,
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_MID = 3,
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_LOW = 4,
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_VERY_LOW = 5,
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_COUNT = 6,
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_INVALID = 7,
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_HIGHEST = 0,
    IO_TASK_PRIORITY_IO_TASK_PRIORITY_LOWEST = 5
};

#pragma pack(push, 4)
class BGSBodyPart
{
  public:
    // is called through vtable slot 0), so MSVC lays out the hidden vptr at
    // +0x0 itself; keeping both would shift every member by 4. The member is
    // therefore dropped and the virtual declared below; all other offsets and
    // the size are preserved verbatim.
    BSStringT<char> NodeName;         // +0x4, 8 bytes
    BSStringT<char> TargetName;       // +0xC, 8 bytes
    BSStringT<char> m_kVATSNodeName;  // +0x14, 8 bytes
    BSStringT<char> m_kPartName;      // +0x1C, 8 bytes
    BSStringT<char> m_kGoreName;      // +0x24, 8 bytes
    TESModel m_kModel;                // +0x2C, 24 bytes
    TESModelPSA m_kRagdollModel;      // +0x44, 24 bytes
    BodyPartInfo Data;                // +0x5C, 84 bytes
    BGSBodyPart();
    ~BGSBodyPart();
    bool Load(TESFile* file);
    void InitItem(TESForm* parent);
    unsigned int FUN_005e3fc0();
    void FUN_00994ef0(BGSImpactDataSet*);
    void FUN_005e3d20();
    void FUN_005e3d50();
    int GetLimb();
    const char* GetPartName();
    virtual void QueueResourceLoad(IO_TASK_PRIORITY priority, QueuedFile* file);
    // BGSBodyPart
    // void __cdecl BGSBodyPart::*()
    // void __cdecl BGSBodyPart::*()
    // void __cdecl BGSBodyPart::*()
    // void __cdecl BGSBodyPart::*()
    // bool __cdecl BGSBodyPart::*(TESFile*)
    // void __cdecl BGSBodyPart::*(TESForm*, BGSBodyPart*)
    // bool __cdecl BGSBodyPart::*(BGSBodyPart*)
    // void __cdecl BGSBodyPart::*(TESForm*)
    // bool __cdecl BGSBodyPart::*()
    // bool __cdecl BGSBodyPart::*()
    // bool __cdecl BGSBodyPart::*()
    // bool __cdecl BGSBodyPart::*()
    // bool __cdecl BGSBodyPart::*()
    // bool __cdecl BGSBodyPart::*()
    // void __cdecl BGSBodyPart::*(bool)
    // bool __cdecl BGSBodyPart::*()
    // void __cdecl BGSBodyPart::*(bool)
    // void __cdecl BGSBodyPart::*(float)
    // float __cdecl BGSBodyPart::*()
    // BGSBodyPart::LIMB_ENUM __cdecl BGSBodyPart::*()
    // float __cdecl BGSBodyPart::*()
    // unsigned char __cdecl BGSBodyPart::*()
    // unsigned char __cdecl BGSBodyPart::*()
    // char __cdecl BGSBodyPart::*()
    // const char* __cdecl BGSBodyPart::*()
    // const char* __cdecl BGSBodyPart::*()
    // const char* __cdecl BGSBodyPart::*()
    // void __cdecl BGSBodyPart::*(char*)
    // const char* __cdecl BGSBodyPart::*()
    // const char* __cdecl BGSBodyPart::*()
    // unsigned char __cdecl BGSBodyPart::*()
    // BGSExplosion* __cdecl BGSBodyPart::*()
    // TESModel* __cdecl BGSBodyPart::*()
    // const char* __cdecl BGSBodyPart::*()
    // BGSDebris* __cdecl BGSBodyPart::*()
    // unsigned char __cdecl BGSBodyPart::*()
    // float __cdecl BGSBodyPart::*()
    // float __cdecl BGSBodyPart::*()
    // BGSImpactDataSet* __cdecl BGSBodyPart::*()
    // unsigned char __cdecl BGSBodyPart::*()
    // BGSExplosion* __cdecl BGSBodyPart::*()
    // BGSDebris* __cdecl BGSBodyPart::*()
    // unsigned char __cdecl BGSBodyPart::*()
    // float __cdecl BGSBodyPart::*()
    // BGSImpactDataSet* __cdecl BGSBodyPart::*()
    // unsigned char __cdecl BGSBodyPart::*()
    // void __cdecl BGSBodyPart::*(BGSExplosion*)
    // void __cdecl BGSBodyPart::*(BGSDebris*)
    // void __cdecl BGSBodyPart::*(BGSImpactDataSet*)
    // void __cdecl BGSBodyPart::*(BGSExplosion*)
    // void __cdecl BGSBodyPart::*(BGSDebris*)
    // void __cdecl BGSBodyPart::*(BGSImpactDataSet*)
    // void __cdecl BGSBodyPart::*(const char*)
    // void __cdecl BGSBodyPart::*(NiPoint3)
    // NiPoint3 __cdecl BGSBodyPart::*()
    // void __cdecl BGSBodyPart::*(NiPoint3)
    // NiPoint3 __cdecl BGSBodyPart::*()
    // void __cdecl BGSBodyPart::*(BGSBodyPart::LIMB_ENUM, NiAVObject*)
    // void __cdecl BGSBodyPart::*(BGSBodyPart::LIMB_ENUM, NiAVObject*)
    // void __cdecl BGSBodyPart::*(BGSBodyPart::LIMB_ENUM, NiAVObject*)
    // bool __cdecl BGSBodyPart::*(NiAVObject*)
    // void __cdecl BGSBodyPart::*()
    // BGSBodyPart& __cdecl BGSBodyPart::*(const BGSBodyPart&)
    // void* __cdecl BGSBodyPart::*(unsigned int)
};
#pragma pack(pop)
FNV_STATIC_ASSERT(sizeof(BGSBodyPart) == 176);
// Note: no offsetof assert for the vtable pointer; it is the compiler-laid-out
// vptr at +0x0 (see member note above), not a declared member.
FNV_STATIC_ASSERT(offsetof(BGSBodyPart, NodeName) == 4);
FNV_STATIC_ASSERT(offsetof(BGSBodyPart, TargetName) == 12);
FNV_STATIC_ASSERT(offsetof(BGSBodyPart, m_kVATSNodeName) == 20);
FNV_STATIC_ASSERT(offsetof(BGSBodyPart, m_kPartName) == 28);
FNV_STATIC_ASSERT(offsetof(BGSBodyPart, m_kGoreName) == 36);
FNV_STATIC_ASSERT(offsetof(BGSBodyPart, m_kModel) == 44);
FNV_STATIC_ASSERT(offsetof(BGSBodyPart, m_kRagdollModel) == 68);
FNV_STATIC_ASSERT(offsetof(BGSBodyPart, Data) == 92);
#endif
