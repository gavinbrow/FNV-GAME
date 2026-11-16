inline void* __cdecl operator new(unsigned int, void* place) { return place; }

struct Entry;
struct Cell { void* value; Cell(){} };
struct Array {
    Cell* data;
    int size;
    unsigned capacity;
};
struct Heap {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    void* allocator;
};
Heap* __cdecl FUN_00c85750();
void __cdecl FUN_00c90940(void*, Array*, int);
struct Actor {
    unsigned short& id() { return *(unsigned short*)((char*)this + 0x22); }
    unsigned char& flags() { return *(unsigned char*)((char*)this + 0x25); }
    void __thiscall FUN_00d07130(Entry*);
};
struct Entry {
    int unk00;
    int unk04;
    int unk08;
    Actor* actor;
    void __thiscall FUN_00c90510();
};
void __cdecl FUN_00cb4790(int* parent, int* elements, Array* output) {
    for (int i = 0; i < *(unsigned short*)&elements[0x83]; i++) {
        Entry* item = ((Entry**)elements[0x82])[i];
        if (item->actor == (Actor*)parent[8]) {
            Heap* heap = FUN_00c85750();
            if (output->size == (int)(output->capacity & 0x3fffffff))
                FUN_00c90940(heap->allocator, output, 4);
            Cell* dst = &output->data[output->size]; new (dst) Cell(); dst->value = item;
            output->size++;
            item->FUN_00c90510();
            ((Actor*)parent[8])->FUN_00d07130(item);
            ((Actor*)parent[8])->flags() = (((Actor*)parent[8])->flags() & 0xdf) | 0x10;
            Actor* actor = (Actor*)parent[8];
            if (actor->id() == 0xffff) {
                actor->id() = (unsigned short)((Array*)&parent[16])->size;
                Array* other = (Array*)&parent[16];
                Heap* heap2 = FUN_00c85750();
                if (other->size == (int)(other->capacity & 0x3fffffff))
                    FUN_00c90940(heap2->allocator, other, 4);
                Cell* dst2 = &other->data[other->size]; new (dst2) Cell(); dst2->value = actor;
                other->size++;
            }
        }
    }
}
