#include <windows.h>
struct LockOwner {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    CRITICAL_SECTION* section;
    void FUN_00d97050();
};
void LockOwner::FUN_00d97050() {
    EnterCriticalSection(section);
}