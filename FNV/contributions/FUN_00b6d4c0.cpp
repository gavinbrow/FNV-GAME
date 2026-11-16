#include "h_21f9ed7f1e0a.h"

class BSMultiBound : public NiObject {
public:
};

struct MultiBoundListItem {
    MultiBoundListItem* m_pkNext;
    MultiBoundListItem* m_pkPrev;
    NiPointer<BSMultiBound> m_element;
};

struct MultiBoundPool {
    unsigned int m_uiCount;
    MultiBoundListItem* FUN_0043a010();
};
struct MultiBoundList {
    MultiBoundListItem* m_pkHead;
    MultiBoundListItem* m_pkTail;
    MultiBoundPool m_allocator;
    void AddTail(const NiPointer<BSMultiBound>& element);
    NiPointer<BSMultiBound> RemovePos(void*& position);
};

struct MultiBoundOwner {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c;
    int unk70; int unk74; int unk78; int unk7c;
    int unk80; int unk84; int unk88; int unk8c;
    MultiBoundList m_kInactiveList;
    MultiBoundList m_kActiveList;
    void FUN_00b6d4c0(BSMultiBound* pkBound);
};

void MultiBoundOwner::FUN_00b6d4c0(BSMultiBound* pkBound)
{
    if (!pkBound)
        return;
    NiPointer<BSMultiBound> spBound;
    MultiBoundListItem* pkItem = m_kActiveList.m_pkHead;
    void* pos = pkItem;
    while (pkItem) {
        spBound = pkItem->m_element;
        if (spBound == pkBound) {
            pos = pkItem;
            break;
        }
        pkItem = pkItem->m_pkNext;
        if (!pkItem) {
            pos = pkItem;
            break;
        }
    }
    if (pos) {
        m_kInactiveList.AddTail(spBound);
        m_kActiveList.RemovePos(pos);
    }
}

void MultiBoundList::AddTail(const NiPointer<BSMultiBound>& element)
{
    MultiBoundListItem* item = m_allocator.FUN_0043a010();
    item->m_element = element;
    item->m_pkNext = 0;
    item->m_pkPrev = m_pkTail;
    if (m_pkTail) m_pkTail->m_pkNext = item;
    else m_pkHead = item;
    ++m_allocator.m_uiCount;
    m_pkTail = item;
}