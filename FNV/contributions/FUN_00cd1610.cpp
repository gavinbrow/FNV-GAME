struct DefaultProcessSlot {
    unsigned int taggedPtr;
    void FUN_00cb0c00();
};
extern "C" int __cdecl FUN_00cb0fa0(unsigned int taggedObject, unsigned int wanted);
struct ErrorMessage {
    void* m_first;
    void* m_second;
    unsigned int m_length;
    unsigned int storage[128];
    void FUN_00cb1600(char* destination, unsigned int capacity);
    ErrorMessage* FUN_00cc01c0(const char* text);
    void FUN_00cc00e0();
};
struct ErrorService {
    virtual void V00();
    virtual void V01();
    virtual void V02();
    virtual void V03(int category, int severity, const char* message, const char* filename, int line);
    virtual void V04();
    virtual void V05();
    virtual void V06();
    virtual void V07(unsigned int key, const char* tag);
    virtual void V08();
};
extern "C" ErrorService* DAT_01268360;
struct FUN_00cd1610_cls {
    unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0c;
    unsigned int unk10; unsigned int unk14; unsigned int unk18; unsigned int unk1c;
    unsigned int unk20; unsigned int unk24; unsigned int unk28; unsigned int unk2c;
    unsigned int unk30; unsigned int unk34; unsigned int unk38; unsigned int unk3c;
    unsigned int unk40; unsigned int unk44; unsigned int unk48; unsigned int unk4c;
    DefaultProcessSlot* m_processes;
    int m_count;
    void FUN_00cd1610(unsigned int wanted);
};
void FUN_00cd1610_cls::FUN_00cd1610(unsigned int wanted) {
    for (int i=0; i < m_count; ++i) {
        unsigned int current = m_processes[i].taggedPtr;
        if (FUN_00cb0fa0(current & ~1u, wanted) == 0) {
            m_processes[i].FUN_00cb0c00();
            --m_count;
            if (m_count != i) {
                DefaultProcessSlot& last = m_processes[m_count];
                m_processes[i] = last;
            }
            return;
        }
    }
    DAT_01268360->V07(0x76565454, "removeDefaultProcess");
    ErrorMessage message;
    message.FUN_00cb1600((char*)message.storage, 512);
    message.FUN_00cc01c0("The default Process'")
        ->FUN_00cc01c0((const char*)wanted)
        ->FUN_00cc01c0("', cannot not be removed from the default process list as it cannot be found!");
    DAT_01268360->V03(0,-1,(char*)message.storage, ".\\hkVisualDebugger.cpp", 318);
    message.FUN_00cc00e0();
    DAT_01268360->V08();
}