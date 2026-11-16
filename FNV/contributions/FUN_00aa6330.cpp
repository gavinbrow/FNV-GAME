#include <windows.h>

struct FUN_00aa6330_Class {
    int unk0;
    unsigned int unk4;
    bool FUN_00aa6330();
};

bool FUN_00aa6330_Class::FUN_00aa6330() {
    unsigned int threadId = GetCurrentThreadId();
    return threadId == unk4;
}
