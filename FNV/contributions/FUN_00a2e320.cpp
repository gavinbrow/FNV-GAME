
struct FNV_MapItem {
    FNV_MapItem* m_pkNext;
    const char* m_pcKey;
    void* m_pkValue;
};
struct FNV_MapView {
    void* m_pVtable;
    unsigned int m_uiHashSize;
    FNV_MapItem** m_ppkHashTable;
    __forceinline FNV_MapItem* GetFirstPos() {
        const unsigned int count = m_uiHashSize;
        unsigned int i = 0;
        if (count > 0) {
            FNV_MapItem** buckets = m_ppkHashTable;
            FNV_MapItem** current = buckets;
            do {
                if (*current != 0)
                    return buckets[i];
                ++i;
                ++current;
            } while (i < count);
        }
        return 0;
    }
    void FUN_00b57f20(FNV_MapItem** position, const char** key, void** value);
    bool FUN_00853130(const char* key, void** value);
};
struct FNV_Comparable {
    virtual void v00(); virtual void v01(); virtual void v02();
    virtual void v03(); virtual void v04(); virtual void v05();
    virtual void v06(); virtual void v07(); virtual void v08();
    virtual void v09(); virtual void v10(); virtual void v11();
    virtual void v12(); virtual void v13(); virtual void v14();
    virtual void v15(); virtual void v16(); virtual void v17();
    virtual void v18(); virtual void v19(); virtual void v20();
    virtual void v21(); virtual void v22();
    virtual bool FUN_00a6cc80(FNV_Comparable* rhs);
};
struct FNV_EqualBase { bool FUN_00a6cc80(FNV_EqualBase* rhs); };
struct FUN_00a2e320_shell : NiControllerManager {
    bool FUN_00a2e320(FUN_00a2e320_shell* rhs);
};

bool FUN_00a2e320_shell::FUN_00a2e320(FUN_00a2e320_shell* rhs) {
    FUN_00a2e320_shell* other = rhs;
    if (!reinterpret_cast<FNV_EqualBase*>(this)->FUN_00a6cc80(reinterpret_cast<FNV_EqualBase*>(other)))
        return false;
    if (m_kSequenceArray.m_usSize != other->m_kSequenceArray.m_usSize)
        return false;

    FNV_MapView* map = reinterpret_cast<FNV_MapView*>(&m_kStringMap);
    FNV_MapItem* position = map->GetFirstPos();
    while (position != 0) {
        const char* key;
        FNV_Comparable* item;
        FNV_Comparable* matchedItem;
        FNV_MapView* otherMap = reinterpret_cast<FNV_MapView*>(&other->m_kStringMap);
        map->FUN_00b57f20(&position, &key, reinterpret_cast<void**>(&item));
        if (!otherMap->FUN_00853130(key, reinterpret_cast<void**>(&matchedItem)))
            return false;
        if (!item->FUN_00a6cc80(matchedItem))
            return false;
    }

    for (unsigned int j = 0; j < m_kSequenceArray.m_usSize; ++j) {
        FNV_Comparable* left = reinterpret_cast<FNV_Comparable*>(m_kSequenceArray.m_pBase[j].m_pObject);
        FNV_Comparable* right = reinterpret_cast<FNV_Comparable*>(other->m_kSequenceArray.m_pBase[j].m_pObject);
        if (left != 0 && right != 0) {
            if (!left->FUN_00a6cc80(right))
                return false;
        } else if (left != right) {
            return false;
        }
    }
    return true;
}
