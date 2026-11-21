// Layout asserts are preserved; the member declarations used by
// fallout_shared/bgsbodypartdata.cpp are added below each class.
#ifndef FNV_TASK_BGSBODYPARTDATA_COPY_H
#define FNV_TASK_BGSBODYPARTDATA_COPY_H

#include "layout_support.h"
#include "BaseFormComponent.h"
#include "TESForm.h"
#include "TESFile.h"
#include "NiPoint3.h"

class BGSBodyPart;
class BGSBodyPartData;
class BGSDebris;
class BGSExplosion;
class BGSImpactDataSet;
class BGSPreloadable;
class BGSRagdoll;
class BSFileEntry;
class BodyPartInfo;
class QueuedFile;
class TESModel;
class TESModelPSA;
class FileEntryList;

#include "BGSBodyPart_native.h"

#pragma pack(push, 4)
class BGSPreloadable : public BaseFormComponent
{
  public:
    // base BaseFormComponent at +0x0, size 4
    BGSPreloadable();
    virtual void QueueResourceLoad(IO_TASK_PRIORITY priority, QueuedFile* file);
    // void __cdecl BGSPreloadable::*()
    // void __cdecl BGSPreloadable::*()
    // void __cdecl BGSPreloadable::*(BaseFormComponent*)
    // bool __cdecl BGSPreloadable::*(BaseFormComponent*)
    // BGSPreloadable
    // BGSPreloadable& __cdecl BGSPreloadable::*(const BGSPreloadable&)
};
#pragma pack(pop)
FNV_STATIC_ASSERT(sizeof(BGSPreloadable) == 4);
#pragma pack(push, 4)
class BGSBodyPartData : public TESForm, public TESModel, public BGSPreloadable
{
  public:
    // base TESForm at +0x0, size 24
    // base TESModel at +0x18, size 24
    // base BGSPreloadable at +0x30, size 4
    BGSBodyPart* m_apBodyParts[15];  // +0x34, 60 bytes
    BGSRagdoll* m_pRagdoll;          // +0x70, 4 bytes
    BGSBodyPartData();
    void ResetFormData();
    virtual void ClearData();
    void ClearBodyParts();
    bool Load(TESFile* file);
    virtual void InitItem();
    void AddBodyPart(BGSBodyPart* part);
    virtual void QueueResourceLoad(IO_TASK_PRIORITY priority, QueuedFile* file);
    static void InitializeBodyPartData();
    static BGSBodyPartData* ms_pBodyPartData;
    static BGSBodyPartData* ms_pBodyPartDataInstance;
    // BGSBodyPartData
    // void __cdecl BGSBodyPartData::*()
    // void __cdecl BGSBodyPartData::*()
    // void __cdecl BGSBodyPartData::*()
    // bool __cdecl BGSBodyPartData::*(TESFile*)
    // void __cdecl BGSBodyPartData::*()
    // BGSBodyPart** __cdecl BGSBodyPartData::*()
    // void __cdecl BGSBodyPartData::*()
    // void __cdecl BGSBodyPartData::*(BGSBodyPart*)
    // void __cdecl BGSBodyPartData::*(NiAVObject*, NiAVObject*, BGSBodyPart::LIMB_ENUM, NiAVObject*)
    // void __cdecl BGSBodyPartData::*(NiAVObject*, NiAVObject*, BGSBodyPart::LIMB_ENUM, NiAVObject*)
    // bool __cdecl BGSBodyPartData::*()
    // bool __cdecl BGSBodyPartData::*(NiNode*)
    // void __cdecl BGSBodyPartData::*(BSDismemberRoots*)
    // void __cdecl BGSBodyPartData::*(BSSimpleList<BGSBodyPart *>*)
    // void __cdecl BGSBodyPartData::*(IO_TASK_PRIORITY, QueuedFile*)
    // void __cdecl BGSBodyPartData::*()
    // BGSRagdoll* __cdecl BGSBodyPartData::*()
    // void __cdecl BGSBodyPartData::*()
    // BGSBodyPartData& __cdecl BGSBodyPartData::*(const BGSBodyPartData&)
    // void __cdecl BGSBodyPartData::*()
};
#pragma pack(pop)
FNV_STATIC_ASSERT(sizeof(BGSBodyPartData) == 116);
FNV_STATIC_ASSERT(offsetof(BGSBodyPartData, m_apBodyParts) == 52);
FNV_STATIC_ASSERT(offsetof(BGSBodyPartData, m_pRagdoll) == 112);
// Unit-local shims for fallout_shared/bgsbodypartdata.cpp Load/InitItem,
// following the accepted bgsimpactdata.h precedent. TESFileFormInt recovers
// the 32-bit GetTESForm the 2008 Load compares with cmp eax,imm.
// resolver. BGSRagdoll is a minimal polymorphic scaffold so InitItem's
// dynamic_cast has a complete target type; only its name matters for codegen
// and manifest RTTI bindings. TESDataHandlerForms extends the minimal canonical
// TESDataHandler with the direct-called AddFormToDataHandler used by
// InitializeBodyPartData (the shared header cannot be edited here).
struct TESFileFormInt : public TESFile
{
    int GetTESForm();
};
struct TESFormInitFlag : public TESForm
{
    bool IsFormInitialized() const;
    static TESForm* GetFormByID(unsigned int formID);
};
class BGSRagdoll : public TESForm
{
  public:
    virtual ~BGSRagdoll();
};
class TESDataHandler
{
};  // only a base for the stand-in below (the unit-local layout_support.h declares no TESDataHandler)
struct TESDataHandlerForms : public TESDataHandler
{
    void AddFormToDataHandler(TESForm* form);
};
extern TESDataHandler* g_dataHandler;
int Warning();
int Warning(const char* format, ...);
#endif
