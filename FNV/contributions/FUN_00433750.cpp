struct ContNode;
bool __fastcall FUN_008256d0(ContNode*);
void* __fastcall FUN_006815c0(void*);
void __cdecl operator delete(void*);
struct ListNode {
    void* m_item;
    ListNode* m_pkNext;
    void FUN_0063f7b0();
};
void __cdecl FUN_00433750(ListNode* param_1)
{
    if (param_1 != 0) {
        while (!FUN_008256d0((ContNode*)param_1)) {
            void* p = *(void**)FUN_006815c0(param_1);
            operator delete(p);
            param_1->FUN_0063f7b0();
        }
    }
}