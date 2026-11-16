#include "pack/h_7765ea49a806.h"

extern int DAT_012681d4;

extern "C" __declspec(dllimport) void* __stdcall TlsGetValue(unsigned long dwTlsIndex);
extern "C" __declspec(dllimport) int __stdcall TlsSetValue(unsigned long dwTlsIndex, void* pvValue);
extern "C" __declspec(dllimport) void __stdcall EnterCriticalSection(void* pkSection);
extern "C" __declspec(dllimport) void __stdcall LeaveCriticalSection(void* pkSection);

struct hkCriticalSectionDataC905 {
    void* m_debugInfo;
    long m_lockCount;
    long m_recursionCount;
    void* m_owningThread;
    void* m_lockSemaphore;
    unsigned long m_spinCount;
};

struct hkReferencedObjectLockC905 {
    int unk00;
    int unk04;
    int m_multiThreaded;
    int m_lockCount;
    int unk10;
    int unk14;
    hkCriticalSectionDataC905 m_section;
};

class hkReferencedObjectC905 : public hkReferencedObject {
public:
    void FUN_00c905b0();
};

void hkReferencedObjectC905::FUN_00c905b0()
{
    if (m_memSizeAndFlags != 0) {
        if (m_referenceCount == 1) {
            m_referenceCount = 0;
            delete this;
            return;
        }
        hkReferencedObjectLockC905* pkLock = reinterpret_cast<hkReferencedObjectLockC905*>(DAT_012681d4);
        const unsigned long& kTls = reinterpret_cast<const unsigned long*>(&DAT_012681d4)[1];
        if (pkLock->m_multiThreaded == 1 && TlsGetValue(kTls) != reinterpret_cast<void*>(0x23df4554)) {
            if (TlsGetValue(kTls) == reinterpret_cast<void*>(0x23df4554)) {
                pkLock->m_lockCount++;
            } else {
                EnterCriticalSection(&pkLock->m_section);
                pkLock->m_lockCount = 1;
                TlsSetValue(kTls, reinterpret_cast<void*>(0x23df4554));
            }
            m_referenceCount--;
            if (--pkLock->m_lockCount <= 0) {
                TlsSetValue(kTls, 0);
                LeaveCriticalSection(&pkLock->m_section);
            }
        } else {
            m_referenceCount--;
        }
    }
}
