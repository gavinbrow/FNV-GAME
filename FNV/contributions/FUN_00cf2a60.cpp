struct PresentFlag { bool value; PresentFlag(bool v):value(v){} PresentFlag(const PresentFlag& v):value(v.value){} };
struct FUN_00cf2a60_t : hkpAabbPhantom {
    void FUN_00ca9520(hkpCollidable* collidable, PresentFlag wasPresent);
    void FUN_00cf2a60(hkpCollidable* collidable);
};
void FUN_00cf2a60_t::FUN_00cf2a60(hkpCollidable* collidable) {
    int index;
    int count = m_overlappingCollidables.m_size;
    int i = 0;
    if (count > 0) {
        void** entry = m_overlappingCollidables.m_data;
        do {
            if (*entry == collidable) { index = i; goto search_done; }
            ++i; ++entry;
        } while (i < count);
    }
    index = -1;
search_done:
    FUN_00ca9520(collidable, PresentFlag(index >= 0));
    if (index >= 0) {
        --m_overlappingCollidables.m_size;
        int lastIndex = m_overlappingCollidables.m_size;
        if (lastIndex != index)
            m_overlappingCollidables.m_data[index] = m_overlappingCollidables.m_data[lastIndex];
        m_orderDirty = 1;
    }
}