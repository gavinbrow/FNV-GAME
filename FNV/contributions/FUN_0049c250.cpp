struct AnimSequenceBase;
struct MapEntry49c250 {
    MapEntry49c250* m_pkNext;
    unsigned short m_usKey;
    AnimSequenceBase* m_pkValue;
};
struct FUN_0049c250_shell {
    virtual ~FUN_0049c250_shell();
    virtual unsigned int KeyToHashIndex(unsigned short key);
    virtual bool IsKeysEqual(unsigned short left, unsigned short right);
    virtual void SetValue(MapEntry49c250* entry, unsigned short key, AnimSequenceBase* value);
    virtual void ClearValue(MapEntry49c250* entry);
    virtual MapEntry49c250* NewItem();
    virtual void DeleteItem(MapEntry49c250* entry);

    unsigned int m_uiHashSize;
    MapEntry49c250** m_ppkHashTable;
    unsigned int m_uiCount;

    bool FUN_0049c250(unsigned short key);
};
bool FUN_0049c250_shell::FUN_0049c250(unsigned short key) {
    unsigned int hashIndex = KeyToHashIndex(key);
    MapEntry49c250* item = m_ppkHashTable[hashIndex];
    if (item != 0) {
        if (IsKeysEqual(key, item->m_usKey)) {
            m_ppkHashTable[hashIndex] = item->m_pkNext;
            ClearValue(item);
            DeleteItem(item);
            m_uiCount -= 1;
            return true;
        }
        else {
        MapEntry49c250* prior = item;
        MapEntry49c250* next = prior->m_pkNext;
        while (next != 0 && !IsKeysEqual(key, next->m_usKey)) {
            prior = next;
            next = next->m_pkNext;
        }
        if (next != 0) {
            prior->m_pkNext = next->m_pkNext;
            ClearValue(next);
            DeleteItem(next);
            m_uiCount -= 1;
            return true;
        }
        }
    }
    return false;
}