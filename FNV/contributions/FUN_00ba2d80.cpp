#include <windows.h>
extern bool DAT_011f94b4;
typedef BOOL (WINAPI *SemaphoreRelease)(HANDLE, LONG, LPLONG);
struct TaskSemaphore {
  volatile long count;
  HANDLE handle;
  void Signal(SemaphoreRelease release) {
    release(handle, 1, 0);
    InterlockedIncrement(&count);
  }
};
struct TaskCompletion {
  volatile long count;
  HANDLE event;
  void Wait() {
    WaitForSingleObject(event, INFINITE);
    InterlockedDecrement(&count);
  }
};
struct RenderTask {
  virtual ~RenderTask();
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
  TaskSemaphore signal;
  unsigned int unk38;
  TaskCompletion completion;
  unsigned int unk44;
  bool stopping;
};
struct RenderTaskManager {
  RenderTask* tasks[2];
  void FUN_00ba2d80();
};
void RenderTaskManager::FUN_00ba2d80() {
  if (DAT_011f94b4) {
    SemaphoreRelease release = &ReleaseSemaphore;
    for (unsigned int index = 0; index < 2; ++index) {
      RenderTask* task = tasks[index];
      if (task) {
        task->stopping = true;
        task->signal.Signal(release);
        task = tasks[index];
        task->completion.Wait();
        delete tasks[index];
        tasks[index] = 0;
      }
    }
  }
}