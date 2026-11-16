struct D47Array {
    int* data;
    int count;
    unsigned int capacityAndFlags;
};
struct D47Router {
    int field00;
    int field04;
    int field08;
    int field0c;
    void* heap;
};
D47Router* __cdecl FUN_00c85750();
void __cdecl FUN_00c90940(void* allocator, D47Array* array, int elementSize);

struct D47Map {
    int FUN_00d87410();
    void FUN_00d874b0(unsigned char* hasNext, int iterator);
    int FUN_00d87440(int iterator);
    int FUN_00d87480(int iterator);
};
struct D47Owner {
    int field00;
    int field04;
    int field08;
    D47Map entries;
    void FUN_00d47bb0(D47Array* values);
};
void D47Owner::FUN_00d47bb0(D47Array* values)
{
    unsigned char hasItem;
    int iterator = entries.FUN_00d87410();
    entries.FUN_00d874b0(&hasItem, iterator);
    while (hasItem) {
        int value = entries.FUN_00d87440(iterator);
        D47Router* router = FUN_00c85750();
        if (values->count == (values->capacityAndFlags & 0x3fffffff)) {
            FUN_00c90940(router->heap, values, 4);
        }
        int* insertion = values->data + values->count;
        ++values->count;
        *insertion = value;
        iterator = entries.FUN_00d87480(iterator);
        entries.FUN_00d874b0(&hasItem, iterator);
    }
}
