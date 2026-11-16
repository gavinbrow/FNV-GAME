#include "h_74712c1d3c73.h"

struct Node {
    Node* m_next;
    void* m_data;
};

struct Queue {
    virtual void vfn0();
    virtual void vfn1();
    virtual void vfn2();
    virtual void vfn3();
    Node* m_head;
    Node* m_tail;
};

bool __cdecl FUN_004491c0(void* destination, void* exchange, void* comperand);

struct QueueConsumer {
    Queue* m_queue;
    Node** m_hp0;
    Node** m_hp1;

    void FUN_006c7560(Node* node);
    bool FUN_006c6fe0(void** out_val);
};

bool QueueConsumer::FUN_006c6fe0(void** out_val) {
    Node* volatile head7 = 0;
    Node* volatile next2;
    Node* tail;

    while (1) {
        head7 = m_queue->m_head;
        m_hp0[0] = head7;
        if (head7 != m_queue->m_head) {
            continue;
        }

        tail = m_queue->m_tail;
        next2 = head7->m_next;
        m_hp1[0] = next2;
        if (head7 != m_queue->m_head) {
            continue;
        }

        if (next2 == 0) {
            m_hp0[0] = 0;
            *out_val = 0;
            return false;
        }

        if (head7 == tail) {
            FUN_004491c0(&m_queue->m_tail, next2, tail);
            continue;
        }

        *out_val = next2->m_data;
        if (FUN_004491c0(&m_queue->m_head, next2, head7)) {
            m_queue->vfn3();
            next2->m_data = 0;
            break;
        }
    }

    m_hp0[0] = 0;
    m_hp1[0] = 0;
    FUN_006c7560(head7);
    return true;
}
