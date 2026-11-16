extern char DAT_010d7ed0;
extern char DAT_010d7eb0;
extern char DAT_010d7e5c;
extern char DAT_010d7cfc;
extern char DAT_010d1508;
extern char DAT_0102e388;
class ProcessManager { public: void FUN_00c99590(void* process); };
extern ProcessManager* DAT_012681e0;
class Process {
public:
    void* vftable;
    int unk04;
    void* baseVftable;
    int unk0c; int unk10; int unk14; int unk18; int unk1c;
    void* listenerVftable;
    void FUN_00ddcb50();
};
void Process::FUN_00ddcb50()
{
    vftable = &DAT_010d7ed0;
    baseVftable = &DAT_010d7eb0;
    listenerVftable = &DAT_010d7e5c;
    DAT_012681e0->FUN_00c99590(&listenerVftable);
    listenerVftable = &DAT_010d7cfc;
    baseVftable = &DAT_010d1508;
    vftable = &DAT_0102e388;
}
