struct LinkedListNode {
    int FUN_005ae380();
    void **FUN_006815c0();
    void FUN_00726c60(void **item);
    LinkedListNode *FUN_00726070();
    void FUN_007a8790(int (__cdecl *compare)(void *, void *));
};
void LinkedListNode::FUN_007a8790(int (__cdecl *compare)(void *, void *))
{
    LinkedListNode *current = this;
    LinkedListNode *previous = 0;
    if (current != 0) {
        int iterations = current->FUN_005ae380();
        bool swapped = true;
        while (iterations && swapped) {
            swapped = false;
            while (current != 0) {
                if (previous != 0) {
                    void *currentItem = *current->FUN_006815c0();
                    void *previousItem = *previous->FUN_006815c0();
                    if (compare(previousItem, currentItem) > 0) {
                        current->FUN_00726c60(&previousItem);
                        previous->FUN_00726c60(&currentItem);
                        swapped = true;
                    }
                }
                previous = current;
                current = current->FUN_00726070();
            }
            --iterations;
        }
    }
}