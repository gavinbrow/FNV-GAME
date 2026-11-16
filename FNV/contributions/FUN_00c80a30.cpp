inline void* __cdecl operator new(unsigned int, void* placement) { return placement; }
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(long volatile* addend);
struct NiAllocator { void* __thiscall FUN_00aa3e40(unsigned int size); };
extern NiAllocator DAT_011f6238;
struct RefObject { int unk00; volatile long referenceCount; };
struct RefNode {
    RefObject* item; RefNode* next;
    __forceinline RefNode(RefObject* p) {
       item = p; if (p) InterlockedIncrement(&p->referenceCount);
       next = 0;
    }
};
struct RefOwner {
    RefObject* item; RefNode* head;
    void __thiscall FUN_006e5cc0(int* param);
    void __thiscall FUN_00c80a30(int* param);
};
void RefOwner::FUN_00c80a30(int* param)
{
    if (*param) {
        if (item) {
            void* memory = DAT_011f6238.FUN_00aa3e40(8);
            RefNode* node = memory ? new (memory) RefNode(item) : 0;
            node->next = head;
            head = node;
            FUN_006e5cc0(param);
            return;
        }
        FUN_006e5cc0(param);
    }
}
