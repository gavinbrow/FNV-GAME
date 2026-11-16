extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);

class NiRefObject {
public:
    virtual void vf00();
    virtual void DeleteThis();
    long m_uiRefCount;
    void DecRefCount() { if (InterlockedDecrement(&m_uiRefCount) == 0) DeleteThis(); }
};

template <class T> class NiPointer {
public:
    T* m_pObject;
    ~NiPointer() { if (m_pObject) m_pObject->DecRefCount(); }
    NiPointer& operator=(T* pObject) {
        if (m_pObject != pObject) {
            if (m_pObject) m_pObject->DecRefCount();
            m_pObject = pObject;
        }
        return *this;
    }
};

struct SharedResource {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
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
    int unk5C;
    int unk60;
    int m_iRefCount;
    void Release();
    void DecRefCount() { int* p = &m_iRefCount; if (--*p == 0) Release(); }
};

template <class T> class RefPtr {
public:
    T* m_pObject;
    RefPtr& operator=(T* pObject) {
        if (m_pObject != pObject) {
            if (m_pObject) m_pObject->DecRefCount();
            m_pObject = pObject;
        }
        return *this;
    }
};

extern NiPointer<NiRefObject> g_aspSmall[2];
extern NiPointer<NiRefObject> g_aspLarge[4];
extern RefPtr<SharedResource> g_spSharedResource;

class ResourceOwnerBase {
public:
    virtual void vf00();
    ~ResourceOwnerBase();
};

class FUN_00bb0550 : public ResourceOwnerBase {
public:
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
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
    int unk5C;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
    int unk74;
    int unk78;
    int unk7C;
    int unk80;
    int unk84;
    int unk88;
    int unk8C;
    int unk90;
    int unk94;
    int unk98;
    NiPointer<NiRefObject> m_spUnk9C;
    virtual void vf00();
    ~FUN_00bb0550();
};

FUN_00bb0550::~FUN_00bb0550()
{
    for (int i = 0; i < 4; i++)
        g_aspLarge[i] = 0;
    for (int i = 0; i < 2; i++)
        g_aspSmall[i] = 0;
    g_spSharedResource = 0;
}
