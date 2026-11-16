class NiRefObject {
public:
    virtual void Destroy();
    virtual void DeleteThis();
    volatile long m_uiRefCount;

    void IncRefCount() {
        ++m_uiRefCount;
    }
    void DecRefCount() {
        if (InterlockedDecrement(&m_uiRefCount) == 0)
            DeleteThis();
    }
};

extern NiPointer<NiRefObject> DAT_01201fc4;

void __cdecl FUN_00bc4610()
{
    DAT_01201fc4 = static_cast<NiRefObject*>(0);
}