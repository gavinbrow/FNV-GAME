
struct PackageSaveWriter {
    void FUN_00857a10(void* data, unsigned int size);
    void FUN_008579b0(void* data, unsigned int size);
};
extern PackageSaveWriter* DAT_011de45c;

struct PackageVirtuals : public TESPackage {
    virtual void Unk_4D();
    virtual void Unk_4E();
    virtual void Unk_4F();
    virtual void Unk_50();
    virtual void Unk_51();
    virtual void Unk_52();
    virtual void Unk_53();
    virtual void Unk_54();
};
struct FUN_008c6250_shell : public ActorPackage {
    void FUN_008c6250(unsigned int auiFlags);
};
void FUN_008c6250_shell::FUN_008c6250(unsigned int auiFlags)
{
    unsigned int uiFormID = 0;
    if (pPackage != NULL) {
        uiFormID = pPackage->GetFormID();
    }
    DAT_011de45c->FUN_00857a10(&uiFormID, 4);
    if (uiFormID != 0) {
        if ((auiFlags & 0) != 0 && g_dataHandler->IsFormIDCreated(uiFormID)) {
            bool bCreated = pPackage->GetIsCreated();
            DAT_011de45c->FUN_008579b0(&bCreated, 1);
            if ((auiFlags & 0) == 0) {
                static_cast<PackageVirtuals*>(pPackage)->Unk_54();
            }
        }
        DAT_011de45c->FUN_008579b0(&iCurrentProcedureIndex, 4);
    }
    DAT_011de45c->FUN_008579b0(&fPackageStartTime, 4);
}
