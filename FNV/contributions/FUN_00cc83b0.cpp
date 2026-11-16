extern __declspec(thread) unsigned int hkThreadAllocationTag;
extern int DAT_010c9f54;
struct AllocationManager {
    void* __thiscall FUN_00aa3e40(unsigned int bytes);
};
extern AllocationManager DAT_011f6238;

struct RefBlock {
    void* vtable;
    void* payload;
    unsigned int referenceCount;
    unsigned int flags;
    unsigned int userData;
};
struct RefBlockArgument { RefBlock* block; };
struct FUN_00cc83b0_Class;
extern "C" void __fastcall FUN_00c89c80(FUN_00cc83b0_Class*, RefBlockArgument);

struct ScopedAllocationTag {
    unsigned int previous;
    ScopedAllocationTag() : previous(hkThreadAllocationTag) {
        hkThreadAllocationTag = 16;
    }
    ~ScopedAllocationTag() {
        hkThreadAllocationTag = previous;
    }
};

struct FUN_00cc83b0_Class {
    void* vtable;
    void* unknown04;
    void* owner;
    void* object;
    void* __thiscall FUN_00cc83b0(bool* created);
};

void* FUN_00cc83b0_Class::FUN_00cc83b0(bool* created) {
    ScopedAllocationTag allocationTag;
    bool missing = (object == 0);
    *created = missing;
    if (missing) {
        RefBlock* block = static_cast<RefBlock*>(DAT_011f6238.FUN_00aa3e40(28));
        void* reference;
        if (block != 0) {
            void** data = &block->payload;
            block->referenceCount = 1;
            block->flags = 0;
            block->userData = 0;
            block->vtable = &DAT_010c9f54;
            *data = 0;
            reference = data;
        } else {
            reference = 0;
        }
        object = reference;
        if (owner != 0) {
            RefBlockArgument header = { reference ? reinterpret_cast<RefBlock*>(static_cast<char*>(reference) - 4) : 0 };
            FUN_00c89c80(this, header);
        }
    }
    return object;
}