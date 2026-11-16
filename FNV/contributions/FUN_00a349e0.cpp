extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(long volatile*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);

extern "C" void* __cdecl FUN_00aa13e0(unsigned int);

extern char* g_pcEmptyFixedString;

struct SeqFixedString {
    char* m_kHandle;
    SeqFixedString(const char* pcString)
    {
        if (pcString == 0)
            m_kHandle = g_pcEmptyFixedString;
        else
            m_kHandle = NiGlobalStringTable::AddString(pcString);
    }
    operator const char*() const { return m_kHandle; }
    ~SeqFixedString()
    {
        if (m_kHandle != g_pcEmptyFixedString)
            InterlockedDecrement((long*)(m_kHandle - 8));
    }
    SeqFixedString& operator=(const SeqFixedString& kString)
    {
        if (m_kHandle != kString.m_kHandle) {
            char* kHandle = kString.m_kHandle;
            if (kHandle != g_pcEmptyFixedString)
                InterlockedIncrement((long*)(kHandle - 8));
            if (m_kHandle != g_pcEmptyFixedString)
                InterlockedDecrement((long*)(m_kHandle - 8));
            m_kHandle = kHandle;
        }
        return *this;
    }
};
namespace a3 { extern SeqFixedString DAT_011f49e0; }

struct SeqRefObject {
    virtual ~SeqRefObject();
    virtual __declspec(nothrow) void DeleteThis() throw();
    long m_uiRefCount;
    void IncRefCount() { InterlockedIncrement(&m_uiRefCount); }
    void DecRefCount() { if (InterlockedDecrement(&m_uiRefCount) == 0) DeleteThis(); }
};

template <class T> struct SeqPtr {
    T* m_pObject;
    SeqPtr(T* p = 0) : m_pObject(p) { if (m_pObject) m_pObject->IncRefCount(); }
    ~SeqPtr() { if (m_pObject) m_pObject->DecRefCount(); }
    SeqPtr& operator=(T* p)
    {
        if (m_pObject != p) {
            if (m_pObject) m_pObject->DecRefCount();
            m_pObject = p;
            if (m_pObject) m_pObject->IncRefCount();
        }
        return *this;
    }
    SeqPtr& operator=(const SeqPtr& p) { return operator=(p.m_pObject); }
    T* operator->() const { return m_pObject; }
    operator T*() const { return m_pObject; }
};

struct SeqTextKeys : SeqRefObject {};

struct SeqController {
    void* vtbl;
    int unk04;
    unsigned short m_uFlags;
    unsigned short unk0A;
    float m_fFrequency;
    float m_fPhase;
    float m_fLoKeyTime;
    float m_fHiKeyTime;
};

struct OldSequence {
    void* vtbl;
    int unk04;
    const char* m_pcName;
    int unk0C;
    void** m_ppObjects;
    unsigned short unk14;
    unsigned short m_usCount;
    int unk18;
    int unk1C;
    SeqController** m_ppControllers;
    int unk24;
    int unk28;
    SeqPtr<SeqTextKeys> m_spTextKeys;
};

struct NewSequence : SeqRefObject {
    static void* __cdecl operator new(unsigned int);
    static void* __cdecl operator new(unsigned int, void* p) { return p; }
    __declspec(noalias) NewSequence(const char* const& kName, unsigned int uiArraySize, unsigned int uiArrayGrowBy) throw();
    __declspec(nothrow) void AddFromOld(void* pkObject, SeqController* pkCtlr) throw();
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    SeqPtr<SeqTextKeys> m_spTextKeys;
    int m_eCycleType;
    float m_fFrequency;
    float m_fBeginKeyTime;
    float m_fEndKeyTime;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    SeqFixedString m_kAccumRootName;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
};

void __cdecl FUN_00a349e0(OldSequence* pkOld, SeqPtr<NewSequence>& spOut) throw()
{
    void* pvRaw = FUN_00aa13e0(0x74);
    unsigned int uiCount = pvRaw != 0 ? pkOld->m_usCount : 0;
    SeqPtr<NewSequence> spSeq = new (pvRaw) NewSequence(SeqFixedString(pkOld->m_pcName), uiCount, uiCount);
    bool bFirst = true;
    for (unsigned int i = 0; i < pkOld->m_usCount; i++) {
        void* pkObject = pkOld->m_ppObjects[i];
        SeqController* pkCtlr = pkOld->m_ppControllers[i];
        if (pkObject && pkCtlr) {
            if (bFirst) {
                int eType = (pkCtlr->m_uFlags >> 1) & 3;
                if (eType != 2 && eType != 0)
                    eType = 0;
                spSeq->m_eCycleType = eType;
                spSeq->m_fFrequency = pkCtlr->m_fFrequency;
                bFirst = false;
                spSeq->m_fBeginKeyTime = pkCtlr->m_fLoKeyTime;
                spSeq->m_fEndKeyTime = pkCtlr->m_fHiKeyTime;
            }
            spSeq->AddFromOld(pkObject, pkCtlr);
        }
    }
    spSeq->m_spTextKeys = pkOld->m_spTextKeys;
    spSeq->m_kAccumRootName = a3::DAT_011f49e0;
    spOut = spSeq;
}
