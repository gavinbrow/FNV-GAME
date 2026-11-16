struct ShaderEntryNode {
    ShaderEntryNode* next;
    ShaderEntryNode* previous;
    void* element;
};
struct ShaderEntryList {
    ShaderEntryNode* head;
    ShaderEntryNode* tail;
    unsigned int count;
    void*& GetNext(ShaderEntryNode*& position) {
        void*& element = position->element;
        position = position->next;
        return element;
    }
    void __thiscall FUN_00b602d0();
    void __thiscall FUN_00e7d5b0();
};
struct ShaderEntryNodePool {
    void* first;
    void __thiscall FUN_0040fbf0(int count);
};
extern ShaderEntryNodePool DAT_011c5f80;
extern ShaderEntryNode* DAT_011c5f58;
extern unsigned int DAT_011c5f84;
extern "C" void __cdecl FUN_00aa10f0(void*);
struct ShaderEntryOwner {
    int unknown00;
    int unknown04;
    ShaderEntryList entries;
    void FUN_00e93cc0();
};
void ShaderEntryOwner::FUN_00e93cc0()
{
    ShaderEntryList* list = &entries;
    ShaderEntryNode* iterator = list->head;
    if (iterator) {
        do {
            void* element = list->GetNext(iterator);
            if (!element)
                continue;
            ShaderEntryNode* head = list->head;
            ShaderEntryNode* candidate;
            ShaderEntryNode* position = list->head;
            if (!position)
                goto release;
            do {
                candidate = position;
                if (element == list->GetNext(position))
                    goto found;
            } while (position);
            goto release;
found:
            if (candidate) {
                if (candidate == head)
                    list->FUN_00b602d0();
                else if (candidate == list->tail)
                    list->FUN_00e7d5b0();
                else {
                    ShaderEntryNode* before = candidate->previous;
                    ShaderEntryNode* after = candidate->next;
                    if (before)
                        before->next = after;
                    if (after)
                        after->previous = before;
                    candidate->element = 0;
                    DAT_011c5f80.FUN_0040fbf0(0);
                    candidate->previous = 0;
                    candidate->next = DAT_011c5f58;
                    --DAT_011c5f84;
                    DAT_011c5f58 = candidate;
                    if (!DAT_011c5f84)
                        DAT_011c5f80.first = 0;
                    --list->count;
                }
            }
release:
            FUN_00aa10f0(element);
        } while (iterator);
    }
}
