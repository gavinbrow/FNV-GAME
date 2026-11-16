struct LinkedNode {
    LinkedNode* previous;
    LinkedNode* next;
};
struct NodeSorter {
    LinkedNode* FUN_00aa70c0(LinkedNode* head);
};
LinkedNode* NodeSorter::FUN_00aa70c0(LinkedNode* head)
{
    LinkedNode *left, *tail, *p, *tailPtr;
    unsigned int insize;
    int i, q, nmerges;
    unsigned int e;
    i = 0;
    if (head == 0)
        return 0;
    insize = 1;
    while (i != 1) {
        left = head;
        head = 0;
        tailPtr = 0;
        i = 0;
        while (left != 0) {
            ++i;
            tail = left;
            nmerges = 0;
            for (e = 0; e < insize; ++e) {
                ++nmerges;
                tail = tail->next;
                if (tail == 0)
                    break;
            }
            q = insize;
            while (nmerges > 0 || (q > 0 && tail != 0)) {

                if (nmerges == 0) {
                    p = tail;
                    tail = tail->next;
                    --q;
                } else if (q == 0 || tail == 0) {
                    p = left;
                    left = left->next;
                    --nmerges;
                } else if (tail >= left) {
                    p = left;
                    left = left->next;
                    --nmerges;
                } else {
                    p = tail;
                    tail = tail->next;
                    --q;
                }
                if (tailPtr != 0)
                    tailPtr->next = p;
                else
                    head = p;
                p->previous = tailPtr;
                tailPtr = p;
            }
            left = tail;
        }
        tailPtr->next = 0;
        insize *= 2;
    }
    return head;
}