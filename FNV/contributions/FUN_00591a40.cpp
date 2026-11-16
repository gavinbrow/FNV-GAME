struct FUN_005ae380_node : BSSimpleList<ItemChange*> {
    int FUN_005ae380();
};

struct FUN_00591a40_fallback {
    int unk00;
    void* FUN_00408da0();
};

struct FUN_00591a40_class {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    FUN_00591a40_fallback m_fallback;
    int unk1C;
    int unk20;
    int unk24;
    FUN_005ae380_node m_list;
    int m_lastIndex;
    void* FUN_00591a40();
};

void* FUN_00591a40_class::FUN_00591a40()
{
    int count = m_list.FUN_005ae380();
    if (m_list.IsEmpty() && count == 0)
        return m_fallback.FUN_00408da0();
    else if (count == 1)
        return m_list.GetItem();
    else {
        BSSimpleList<ItemChange*>* node = &m_list;
        int index = GetRandomNumberInRange(0, m_list.FUN_005ae380());

        if (m_lastIndex != 0 && m_lastIndex == index) {
            index = 0;
            m_lastIndex = index;
        } else if (m_lastIndex == 0 && m_lastIndex == index) {
            index = 1;
            m_lastIndex = index;
        } else {
            m_lastIndex = index;
        }

        while (node != 0 && index--) {
            node = node->GetNext();
        }

        if (node != 0 && node->GetItem() != 0)
            return node->GetItem();
    }

    return m_fallback.FUN_00408da0();
}