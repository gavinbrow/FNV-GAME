template <int SIZE>
__forceinline void memCpyOneAlignedD60E(void* dst, const void* src)
{
    const unsigned int* s = (const unsigned int*)src;
    unsigned int* d = (unsigned int*)dst;
    int i = 0;
    do {
        d[i] = s[i];
    } while (++i < SIZE / 4);
}

struct hkMemoryRouterD60E {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    void* m_heap;
};

namespace hkRouterD60E {
    extern "C" hkMemoryRouterD60E& __cdecl FUN_00c85750() throw();
}
void __cdecl FUN_00c90940(void* pHeap, void* pArray, int iSizeElem);

template <class T>
class hkArrayD60E {
public:
    T* m_data;
    int m_size;
    int m_capacityAndFlags;

    int getCapacity() const { return m_capacityAndFlags & 0x3fffffff; }
    __forceinline void pushBack(const T& e)
    {
        hkMemoryRouterD60E& router = hkRouterD60E::FUN_00c85750();
        if (m_size == getCapacity())
            FUN_00c90940(router.m_heap, this, sizeof(T));
        memCpyOneAlignedD60E<sizeof(T)>(m_data + m_size, &e);
        m_size++;
    }
};

class ListenerD60E {
public:
    virtual int FUN_00d60e80(int iId);
};

class EntryD60E {
public:
    virtual void vfn_00();
    virtual void vfn_04();
    virtual void vfn_08();
    virtual void vfn_0C();
    virtual void vfn_10();
    virtual void vfn_14();
    int unk04;
    int m_unk08;
    int m_unk0C;
    int m_unk10;
    ListenerD60E* m_pkListener;
};

class EntryFactoryD60E {
public:
    EntryD60E* FUN_00dd92f0(int iId, void* pvParam);
};

class EntryListD60E {
public:
    void FUN_00dd9600(EntryD60E* pkEntry);
};

class OwnerBaseD60E {
public:
    virtual void vfn_00();
    int unk04;
};

class OwnerD60E : public OwnerBaseD60E, public ListenerD60E {
public:
    int unk0C;
    int unk10;
    int m_unk14;
    int m_unk18;
    int m_unk1C;
    int unk20;
    EntryListD60E m_kEntryList;
    int unk28, unk2C, unk30, unk34;
    hkArrayD60E<EntryD60E*> m_kEntries;
    int m_unk44;

    int FUN_00d60d40(int iId);
    virtual int FUN_00d60e80(int iId);
};

int OwnerD60E::FUN_00d60e80(int iId)
{
    if (FUN_00d60d40(iId) >= 0)
        return 0;
    EntryD60E* pkEntry = ((EntryFactoryD60E*)DAT_01269cd0)->FUN_00dd92f0(iId, &m_unk44);
    if (pkEntry) {
        EntryD60E* const receiver = pkEntry;
        receiver->m_unk08 = m_unk14;
        receiver->m_unk0C = m_unk18;
        receiver->m_pkListener = this;
        receiver->m_unk10 = m_unk1C;
        receiver->vfn_14();
        m_kEntries.pushBack(pkEntry);
        m_kEntryList.FUN_00dd9600(pkEntry);
        return 0;
    }
    return 1;
}
