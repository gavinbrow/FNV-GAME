
struct ShapeAlloc;
struct ShapeRouter {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    ShapeAlloc* m_heap;
    ShapeAlloc& heap() { return *m_heap; }
};
void __cdecl FUN_00c908c0(void* allocator, void* array, int capacity, int elementSize);
void __cdecl FUN_00c90670(void* data, int count, int elementSize);

struct ListShapeCF54 : public hkpListShape {
    void FUN_00cf5420();
    void FUN_00cf54d0(int* shapes, int count, int* shapeData, int flag);
};

void ListShapeCF54::FUN_00cf54d0(int* shapes, int count, int* shapeData, int flag)
{
    hkArray<hkpListShapeChildInfo>& children = m_childInfo;
    ShapeAlloc& heap = reinterpret_cast<ShapeRouter*>(FUN_00c85750())->heap();
    int capacity = children.m_capacityAndFlags & 0x3fffffff;
    if (capacity < count) {
        int increasedCapacity = capacity * 2;
        if (count >= increasedCapacity)
            increasedCapacity = count;
        FUN_00c908c0(&heap, &children, increasedCapacity, 16);
    }
    children.m_size = count;
    if (count > 0) {
        int* current = shapes;
        int offset = 0;
        volatile int difference = (int)shapeData - (int)shapes;
        int remaining = count;
        do {
            int shape = *current;
            if (shape) {
                *(int*)((char*)children.m_data + offset) = shape;
                int filter = shapeData ? *(int*)((char*)current + difference) : 0;
                *(int*)((char*)children.m_data + offset + 4) = filter;
                *(int*)((char*)this->m_childInfo.m_data + offset + 12) = count;
                *(int*)((char*)this->m_childInfo.m_data + offset + 8) = 0;
            }
            ++current;
            offset += 16;
        } while (--remaining);
    }
    if (flag == 1)
        FUN_00c90670(children.m_data, this->m_childInfo.m_size, 16);
    FUN_00cf5420();
}
