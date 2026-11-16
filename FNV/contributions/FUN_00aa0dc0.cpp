#include "h_7349019299ad.h"

struct S_00aa0d00_Node {
    S_00aa0d00_Node* next;
    S_00aa0d00_Node* prev;
    void* data;
};

struct S_00aa0d00_Aux {
    int unk00;
    void FUN_0040fbf0(int a);
};

extern S_00aa0d00_Aux DAT_011c5f80;
extern S_00aa0d00_Node* DAT_011c5f58;
extern unsigned int DAT_011c5f84;

extern int DAT_010a23ac;
extern int DAT_010a2304;

extern void NiFree(void*);

struct C_00aa0dc0 : NiBackToFrontAccumulator {
    void FUN_00aa0dc0();
};

void C_00aa0dc0::FUN_00aa0dc0() {
    NiBackToFrontAccumulator* self = this;

    *(unsigned int*)self = (unsigned int)&DAT_010a23ac;
    NiFree(self->m_ppkItems);
    NiFree(self->m_pfDepths);

    while (self->m_kItems.m_uiCount != 0) {
        S_00aa0d00_Node* item = (S_00aa0d00_Node*)self->m_kItems.m_pkHead;

        self->m_kItems.m_pkHead = (NiBackToFrontListItem*)item->next;
        if (self->m_kItems.m_pkHead != 0) {
            self->m_kItems.m_pkHead->m_pkPrevious = 0;
        } else {
            self->m_kItems.m_pkTail = 0;
        }

        item->data = 0;
        DAT_011c5f80.FUN_0040fbf0(0);
        item->prev = 0;
        item->next = DAT_011c5f58;

        --DAT_011c5f84;
        DAT_011c5f58 = item;
        if (DAT_011c5f84 == 0) {
            DAT_011c5f80.unk00 = 0;
        }

        --self->m_kItems.m_uiCount;
    }

    self->m_kItems.FUN_00b71300();
    *(unsigned int*)self = (unsigned int)&DAT_010a2304;
    self->FUN_00a5d3d0();
}
