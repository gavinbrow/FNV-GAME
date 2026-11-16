#include <windows.h>
struct SyncSemaphore {
    volatile LONG count;
    HANDLE handle;
};
struct AudioWorker {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    SyncSemaphore waitSemaphore;
    unsigned int unk38;
    SyncSemaphore signalSemaphore;
    unsigned int unk44;
    bool processing;
    void FUN_00ae7a50();
};
void AudioWorker::FUN_00ae7a50() {
    processing = true;
    SyncSemaphore* signal = &signalSemaphore;
    ReleaseSemaphore(signal->handle, 1, 0);
    InterlockedIncrement(&signal->count);
    SyncSemaphore* waiting = &waitSemaphore;
    WaitForSingleObject(waiting->handle, INFINITE);
    InterlockedDecrement(&waiting->count);
    processing = false;
}
