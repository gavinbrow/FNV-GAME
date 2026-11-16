#include <windows.h>

struct CriticalSectionOwner {
    int refCount;
    int mode04;
    int mode08;
    int hasValue;
    int flags10;
    int* criticalSection;
    int data18;
    int data1c;
    int data20;
    int data24;
    int value28;
};
void __stdcall FUN_009f9bb0(FUN_009f9a30_class* target, int* value);

struct CriticalSectionGuard {
    int* section;
    explicit CriticalSectionGuard(int* p) : section(p) {
        EnterCriticalSection(reinterpret_cast<LPCRITICAL_SECTION>(section));
    }
    ~CriticalSectionGuard() {
        LeaveCriticalSection(reinterpret_cast<LPCRITICAL_SECTION>(section));
    }
};
int __stdcall FUN_009fc390(CriticalSectionOwner* owner, FUN_009f9a30_class* target) {
    if (!target) {
        return 0x80004003;
    }
    CriticalSectionGuard guard(owner->criticalSection);
    if (owner->hasValue != 0) {
        FUN_009f9bb0(target, &owner->value28);
        return 0;
    }
    target->FUN_009f9a30();
    return 0x80040209;
}
