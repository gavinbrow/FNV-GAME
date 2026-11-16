#include <windows.h>
extern bool DAT_011f94b4;
struct WorkerSync {
    volatile LONG activeCount;
    HANDLE semaphore;
};
struct WorkerState {
    void* unk00; void* unk04; void* unk08; void* unk0c;
    void* unk10; void* unk14; void* unk18; void* unk1c;
    void* unk20; void* unk24; void* unk28; void* unk2c;
    WorkerSync synchronization;
};
class ThreadCoordinator {
public:
    WorkerState* workers[2];
    unsigned int unk08;
    volatile unsigned int counters[2];
    void FUN_00ba2f30();
};
void ThreadCoordinator::FUN_00ba2f30() {
    if (!DAT_011f94b4) return;
    volatile unsigned int* current = counters;
    unsigned int remaining = 2;
    do {
        *current++ = 0;
    } while (--remaining);
    for (unsigned int index = 0; index < 2; ++index) {
        WorkerState* worker = workers[index];
        if (worker != 0) {
            WorkerSync* synchronization = &worker->synchronization;
            ReleaseSemaphore(synchronization->semaphore, 1, 0);
            InterlockedIncrement(&synchronization->activeCount);
        }
    }
}