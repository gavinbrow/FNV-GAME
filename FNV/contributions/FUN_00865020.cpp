extern "C" const char DAT_01082228[];
struct FUN_008c71b0 {
    unsigned int value;
    explicit FUN_008c71b0(unsigned int v);
    FUN_008c71b0(const FUN_008c71b0& other);
};
struct SaveContext_00851110 { void* FUN_00851110(); };
extern "C" SaveContext_00851110* DAT_011de134;
struct FUN_008659c0_Buffer {
    void* vtable; char* data; char* next; char* end;
    unsigned int capacity; unsigned int offset; TESForm* form;
    unsigned int flags; void* stream;
    FUN_008659c0_Buffer();
    ~FUN_008659c0_Buffer();
    void FUN_00865ad0(unsigned int formID, FUN_008c71b0 flags, TESBoundObject* base, void* context);
    void FUN_0050f9c0(TESForm* form);
};
struct TESObjectREFR_00401170 : TESObjectREFR {
    TESBoundObject* FUN_00401170();
};
struct FUN_00865020_Shell {
    char* pBuffer;
    void FUN_00865120(FUN_008659c0_Buffer* buffer);
    void FUN_00865020(TESForm* form);
};
void FUN_00865020_Shell::FUN_00865020(TESForm* form) {
    if (form->GetIsReference()) {
        TESObjectREFR* ref = static_cast<TESObjectREFR*>(form);
        FUN_008659c0_Buffer buffer;
        buffer.FUN_00865ad0(form->GetFormID(), FUN_008c71b0(4),
                         static_cast<TESObjectREFR_00401170*>(form)->FUN_00401170(),
                         DAT_011de134->FUN_00851110());
        buffer.FUN_0050f9c0(form);
        ref->LoadAnimation(reinterpret_cast<BGSLoadFormBuffer*>(&buffer));
        FUN_00865120(&buffer);
    } else {
        SaveGameWarning(DAT_01082228, form->GetName(), form->GetFormID());
    }
}