extern "C" unsigned char __fastcall FUN_008256d0(void*);
extern "C" TESForm** __fastcall FUN_006815c0(void*);
extern "C" void* __fastcall FUN_00726070(void*);
int __cdecl FUN_00404dc0(const char*,const char*);
struct FUN_00461700_shell {
    TESForm* FUN_00461700(const char* editorID);
};
TESForm* FUN_00461700_shell::FUN_00461700(const char* editorID) {
    if (!FUN_008256d0((char*)this + 0xe8)) {
        TESForm* form;
        void* node = (char*)this + 0xe8;
        while (node != 0) {
            form = *FUN_006815c0(node);
            if (form != 0) {
                if (FUN_00404dc0(form->GetEditorID(), editorID) == 0) {
                    return form;
                }
            }
            node = FUN_00726070(node);
        }
    }
    return 0;
}