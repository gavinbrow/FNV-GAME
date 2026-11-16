struct VertexRecord {
    int x, y, z, w;
    ~VertexRecord() {}
    void FUN_00a27430(int);
    static void* operator new[](unsigned int size) { return ((P03MM*)&g_memoryManager)->Allocate(size); }
};
VertexRecord* __cdecl FUN_00a2a8e0(int v, unsigned int count)
{
    VertexRecord* items = new VertexRecord[count];
    for (unsigned int i = 0; i < count; ++i)
        items[i].FUN_00a27430(v);
    return items;
}