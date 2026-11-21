#ifndef FNV_EXPERIMENT_TESMODEL_H
#define FNV_EXPERIMENT_TESMODEL_H
#include "BaseFormComponent.h"
#include "FileEntryList_native.h"
class TESFile;
class TESModelTextureSwap;
#pragma pack(push, 4)
class TESModel : public BaseFormComponent
{
  public:
    BSStringT<char> m_kModelFilePath;
    FileEntryList m_pTextureSwapData;
    unsigned char cFlags, layoutPadding15[3];
    virtual void Init();
    virtual void Free();
    virtual void CopyFromBase(BaseFormComponent*);
    virtual bool CompareWithBase(BaseFormComponent*);
    virtual ~TESModel();
    virtual const char* vfn_14();
    virtual void vfn_18(const char*);
    virtual TESModelTextureSwap* GetAsModelTextureSwap();
    static void LoadModelData(TESModel*, TESFile*);
    static void LoadTextureSwapData(TESModel*, TESFile*);
    TESModel();
    unsigned int GetModelLength() const;
};
#pragma pack(pop)
FNV_STATIC_ASSERT(sizeof(TESModel) == 24);
#endif
