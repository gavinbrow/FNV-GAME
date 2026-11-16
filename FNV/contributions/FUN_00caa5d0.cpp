struct Allocator9 { void* __thiscall FUN_00aa3e40(unsigned int size); };
extern Allocator9 DAT_011f6238;
extern "C" int DAT_010c5dc0;
extern __declspec(thread) unsigned char threadContext9;
struct Guard9 {
    int previous;
    Guard9() {
        int* flag = (int*)((char*)&threadContext9 + 0x2b4);
        previous = *flag;
        *flag = 16;
    }
    ~Guard9() {
        int* flag = (int*)((char*)&threadContext9 + 0x2b4);
        *flag = previous;
    }
};
struct Node9 { void* vtable; int value; int references; int previous; int next; };
struct Class9 {
    void* unk00; void* unk04; int callbackFlag; int* data;
    void __thiscall FUN_00c89c80(Node9* node);
    int* __thiscall FUN_00caa5d0(unsigned char* wasEmpty);
};
int* Class9::FUN_00caa5d0(unsigned char* wasEmpty) {
    Guard9 guard;
    *wasEmpty = (data == 0);
    if (*wasEmpty) {
        Node9* allocated = (Node9*)DAT_011f6238.FUN_00aa3e40(20);
        int* nextData;
        if (allocated) {
            int* contents = &allocated->value;
            allocated->references = 1;
            allocated->previous = 0;
            allocated->next = 0;
            allocated->vtable = &DAT_010c5dc0;
            *contents = 0;
            nextData = contents;
        } else nextData = 0;
        data = nextData;
        if (callbackFlag) FUN_00c89c80(data ? (Node9*)((char*)data - 4) : 0);
    }
    return data;
}