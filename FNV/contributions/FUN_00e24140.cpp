struct Node
{
    Node* next;
    Node* previous;
    Node* FUN_00e22ec0(Node* source);
};
struct Manager {};
struct Object { Manager* manager; };
struct This
{
    Object* object;
    int ready;
    int unk08;
    Node* head;
    unsigned int count;
    Manager* FUN_00e23530();
    void FUN_00e24140(Node* volatile source);
};
void This::FUN_00e24140(Node* volatile source)
{
    Node* node;
    {
        Manager* manager;
        if (ready != 0 && *(Node**)((char*)object->manager + 0xa00) != 0)
            manager = object->manager;
        else
            manager = FUN_00e23530();
        Node** freeHead = (Node**)((char*)manager + 0xa00);
        node = *freeHead;
        Node* next = node->next;
        ++*(unsigned int*)((char*)manager + 0xa04);
        *freeHead = next;
    }
    Node* argument = source;
    node = node->FUN_00e22ec0(argument);
    node->previous = 0;
    node->next = head;
    if (head) head->previous = node;
    ++count;
    head = node;
}




