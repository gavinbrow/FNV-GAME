struct Item_00863bc0 {
    Item_00863bc0* m_pkNext;
    unsigned char m_key;
    unsigned int m_val;
};

struct Map_00863bc0 {
    virtual void Vfn0() = 0;
    virtual unsigned int Hash(unsigned char key) = 0;
    unsigned int m_uiCount;
    Item_00863bc0** m_ppBuckets;
    void FUN_00863bc0(Item_00863bc0*& item, unsigned char& key, unsigned int& val);
};

void Map_00863bc0::FUN_00863bc0(Item_00863bc0*& item, unsigned char& key, unsigned int& val)
{
    Item_00863bc0* pkItem = item;
    unsigned int uiIndex;
    key = pkItem->m_key;
    val = pkItem->m_val;
    if (pkItem->m_pkNext != 0) {
        item = pkItem->m_pkNext;
        return;
    }
    uiIndex = Hash(pkItem->m_key);
    uiIndex++;
    for (; uiIndex < m_uiCount; uiIndex++) {
        pkItem = m_ppBuckets[uiIndex];
        if (pkItem != 0) {
            item = pkItem;
            return;
        }
    }
    item = 0;
}
