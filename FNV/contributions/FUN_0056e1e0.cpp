struct ListHead
{
    void* item;
    void* next;
    ListHead();
};

struct ListTail
{
    void* item;
    ListTail();
    void FUN_005407b0(int value);
};

struct GuardedMember
{
    void* value;
    GuardedMember();
    ~GuardedMember();
};

struct FUN_0056e1e0
{
    ListHead head;
    ListTail tail;
    GuardedMember guarded;
    FUN_0056e1e0();
};

FUN_0056e1e0::FUN_0056e1e0()
{
    head.item = 0;
    head.next = 0;
    tail.FUN_005407b0(1);
}