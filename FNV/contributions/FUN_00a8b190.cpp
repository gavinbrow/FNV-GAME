#include <string.h>
struct MMAllocInterface { void* FUN_00aa3e40(unsigned int); };
struct ArrayElement {
    unsigned int value;
    static void* operator new[](unsigned int bytes) {
        return ((MMAllocInterface*)&g_memoryManager)->FUN_00aa3e40(bytes);
    }
};
MyObj* __fastcall FUN_00a8b190(MyObj* self, void*, const MyObj* rhs)
{
    if (self != rhs) {
        if (self->f18) {
            delete reinterpret_cast<RendererData*>(self->f18);
            self->f18 = 0;
        }
        self->f08 = rhs->f08;
        self->f10 = 1;
        if (self->f0C != rhs->f0C) {
            g_memoryManager._DeallocateAlias((void*)self->f14);
            unsigned int count = (unsigned int)rhs->f0C;
            self->f0C = (void*)count;
            self->f14 = (int)(new ArrayElement[count]);
        }
        memcpy((void*)self->f14, (void*)rhs->f14, (unsigned int)rhs->f0C * sizeof(int));
    }
    return self;
}
