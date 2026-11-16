extern "C" __declspec(dllimport) void* __stdcall GetCurrentProcess(void);
extern "C" __declspec(dllimport) int __stdcall FreeLibrary(void* hLibModule);
extern int DAT_010d4de4;
extern int DAT_0102e388;
struct FUN_00da2930_Loader {
    void* hModule;
    int unk04,unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24,unk28;
    void (__stdcall* releaseProcess)(void*);
};
struct FUN_00da2930_Class {
    void* vtable;
    int unk04;
    FUN_00da2930_Loader* loader;
    void FUN_00da2930();
};
void FUN_00da2930_Class::FUN_00da2930() {
    FUN_00da2930_Loader* p = loader;
    vtable = &DAT_010d4de4;
    if (p->hModule) {
        p->releaseProcess(GetCurrentProcess());
        void* module = p->hModule;
        p->unk08=0; p->unk0c=0; p->unk10=0; p->unk14=0; p->unk18=0;
        p->unk1c=0; p->unk20=0; p->unk24=0; p->unk28=0;
        p->releaseProcess=0;
        FreeLibrary(module);
        p->hModule=0;
    }
    vtable=&DAT_0102e388;
}