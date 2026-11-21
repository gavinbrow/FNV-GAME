#ifndef FNV_PHASE2_TESCONTAINER_H
#define FNV_PHASE2_TESCONTAINER_H
#include "BaseFormComponent.h"
class TESForm;
class TESObject;
class InventoryStackRecord;
class InventoryItemEntry;
#pragma pack(push, 4)
class TESContainer : public BaseFormComponent
{
  public:
    BSSimpleList<InventoryStackRecord*> objectList;
    virtual void Init();
    BSSimpleList<InventoryStackRecord*>* GetObjectList();
    void AddObject(InventoryItemEntry* object);
    void ClearObjects();
    void InitItem(TESForm* form);
    virtual void Free();
    virtual void CopyFromBase(BaseFormComponent* component);
    virtual bool CompareWithBase(BaseFormComponent* other);
    ~TESContainer();
    bool HasObjectOfType(TESObject* object);
    int GetObjectCount(TESObject* object);
    static bool IsValidContainerType(unsigned char type);
    TESContainer();
};
#pragma pack(pop)
FNV_STATIC_ASSERT(sizeof(TESContainer) == 0xC);
#endif
