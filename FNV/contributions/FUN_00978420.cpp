
struct EventCollection {
    unsigned int FUN_005de0f0(unsigned int option);
    unsigned int FUN_005be5c0(unsigned int option);
    void* FUN_00968670(unsigned int index);
};
struct FUN_00978420_shell {
    void* m_pVirtualTable;
    EventCollection m_events;
    void FUN_00978420(float elapsedTime, unsigned int unused);
};
void FUN_00978420_shell::FUN_00978420(float elapsedTime, unsigned int unused) {
    void* currentEvent = 0;
    void* activeEvent = 0;
    for (unsigned int index = m_events.FUN_005de0f0(0);
         index < m_events.FUN_005be5c0(0);
         ++index) {
        currentEvent = m_events.FUN_00968670(index);
        if (currentEvent != 0) {
            typedef bool (__thiscall* IsReadyProc)(void*);
            if ((*reinterpret_cast<IsReadyProc**>(currentEvent))[0x100 / 4](currentEvent)) {
                activeEvent = currentEvent;
                typedef void (__thiscall* UpdateProc)(void*, float);
                (*reinterpret_cast<UpdateProc**>(activeEvent))[0x268 / 4](activeEvent, elapsedTime);
            }
        }
    }
}
