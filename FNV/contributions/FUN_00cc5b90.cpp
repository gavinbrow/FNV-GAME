extern int DAT_01268188;
extern int DAT_012685f4;
extern int DAT_0108febc;
extern int DAT_010c52bc;
extern __declspec(thread) int g_ThreadData;
extern void* __cdecl FUN_00aa13e0(unsigned int bytes);
void __cdecl FUN_00c876f0();
void __cdecl FUN_00c87700();
void __cdecl FUN_00aa4060(void* p);

struct S_00cc5b90_Node
{
    int* vtable;
    int data04;
    int data08;
    int data0c;
    void __thiscall FUN_00c87c30();
};
struct S_00cc5b90_Scope
{
    volatile int savedState;
    S_00cc5b90_Scope()
    {
        int* currentState = reinterpret_cast<int*>(
            reinterpret_cast<char*>(&g_ThreadData) + 0x2b4);
        savedState = *currentState;
        *currentState = 16;
    }
    __forceinline ~S_00cc5b90_Scope()
    {
        int* currentState = reinterpret_cast<int*>(
            reinterpret_cast<char*>(&g_ThreadData) + 0x2b4);
        *currentState = savedState;
    }
};
struct S_00cc5b90_PendingAllocation
{
    S_00cc5b90_Node* object;
    explicit S_00cc5b90_PendingAllocation(S_00cc5b90_Node* p) : object(p) {}
    __forceinline ~S_00cc5b90_PendingAllocation() { if (object) FUN_00aa4060(object); }
    void Transfer() { object = 0; }
};
struct S_00cc5b90_Owner
{
    void __thiscall FUN_00c89730(S_00cc5b90_Node*, int);
    S_00cc5b90_Node* __thiscall FUN_00cc5b90(int arg);
};
S_00cc5b90_Node* __thiscall S_00cc5b90_Owner::FUN_00cc5b90(int arg)
{
    S_00cc5b90_Scope scope;
    FUN_00c876f0();
    S_00cc5b90_Node* result;
    {
        S_00cc5b90_PendingAllocation allocation(static_cast<S_00cc5b90_Node*>(FUN_00aa13e0(16)));
        S_00cc5b90_Node* rawObject = allocation.object;
        if (rawObject)
        {
            rawObject->FUN_00c87c30();
            rawObject->vtable = &DAT_0108febc;
            rawObject->data0c = 0;
            ++DAT_01268188;
            rawObject->vtable = &DAT_010c52bc;
            ++DAT_012685f4;
            result = rawObject;
        }
        else
        {
            result = 0;
        }
        allocation.Transfer();
    }
    FUN_00c89730(result, arg);
    FUN_00c87700();
    return result;
}
