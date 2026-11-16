struct QueueNode {
    unsigned int id;
    unsigned int status;
    void* handler;
    QueueNode* next;
    ~QueueNode();
};
struct HandlerArgument {
    unsigned int type;
    unsigned int data;
    unsigned int flags;
    HandlerArgument(int value);
    ~HandlerArgument();
};
struct QueueOwner {
    unsigned int state;
    unsigned int capacity;
    unsigned int flags;
    QueueNode* first;
    void __thiscall FUN_00418900(const HandlerArgument& argument);
    void __thiscall FUN_0076b7a0();
};
void QueueOwner::FUN_0076b7a0()
{
    while (first != 0) {
        QueueNode* next = first->next;
        first->next = 0;
        delete first;
        first = next;
    }
    FUN_00418900(HandlerArgument(0));
}