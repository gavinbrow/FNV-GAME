#include <xmmintrin.h>
struct __declspec(align(16)) Vertex {
    __m128 value;
};
struct Edge { int polygon, end, start, adjacent; };
template<class T> struct DynamicArray {
    T* data;
    int size;
    unsigned int capacityAndFlags;
    DynamicArray() : data(0), size(0), capacityAndFlags(0x80000000u) {}
};
struct GeometryBuffers {
    DynamicArray<Vertex> vertices;
    DynamicArray<Edge> edges;
    GeometryBuffers() : vertices(), edges() {}
    static void* operator new(unsigned int, void* position) { return position; }
};
struct Allocator {
    virtual void unused();
    virtual void* __thiscall Allocate(unsigned int);
};
struct GlobalContext {
    int unk00, unk04, unk08, unk0c;
    Allocator* allocator;
};
extern "C" GlobalContext* __cdecl FUN_00c85750();
extern "C" void __cdecl FUN_00c90940(Allocator*, DynamicArray<Vertex>*, int);
extern "C" void __cdecl FUN_00c908c0(Allocator*, DynamicArray<Edge>*, int, int);
struct ForwardArg { GeometryBuffers* value; };
struct MeshBuilder;
extern "C" void __fastcall FUN_00de54b0(MeshBuilder*, ForwardArg);
struct MeshBuilder {
    int unk00;
    int unk04;
    GeometryBuffers* geometry;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    Vertex initialVertex;
    int unk70, unk74, unk78, unk7c;
    volatile int segmentCount;
    void __thiscall FUN_00de57a0();
};
void __thiscall MeshBuilder::FUN_00de57a0() {
    GlobalContext* context = FUN_00c85750();
    Allocator* resourceAllocator = context->allocator;
    GeometryBuffers* raw = static_cast<GeometryBuffers*>(
       resourceAllocator->Allocate(sizeof(GeometryBuffers)));
    GeometryBuffers* buffers = raw ? new(raw) GeometryBuffers() : 0;
    geometry = buffers;
    ForwardArg arg; arg.value = buffers;
    FUN_00de54b0(this,arg);
    DynamicArray<Vertex>& vertices = geometry->vertices;
    GlobalContext* manager = FUN_00c85750();
    if (vertices.size == (vertices.capacityAndFlags & 0x3fffffffu)) {
        FUN_00c90940(manager->allocator, &vertices, sizeof(Vertex));
    }
    __m128 value = _mm_load_ps(reinterpret_cast<const float*>(&initialVertex));
    _mm_store_ps(reinterpret_cast<float*>(&vertices.data[vertices.size]), value);
    ++vertices.size;
    DynamicArray<Edge>& edges = geometry->edges;
    int required = segmentCount;
    GlobalContext* manager2 = FUN_00c85750();
    Allocator* edgeAllocator = manager2->allocator;
    int capacity = edges.capacityAndFlags & 0x3fffffffu;
    if (capacity < required) {
        int newCapacity = capacity * 2;
        if (required >= newCapacity) newCapacity = required;
        FUN_00c908c0(edgeAllocator, &edges, newCapacity, sizeof(Edge));
    }
    edges.size = required;
    int index = 0;
    int noAdjacent = -1;
    int initialCount = segmentCount;
    --initialCount;
    if (initialCount > 0) {
        do {
            Edge& entry = geometry->edges.data[index];
            entry.polygon = segmentCount;
            entry.end = index+1;
            entry.start = index;
            entry.adjacent = noAdjacent;
            ++index;
        } while (index < segmentCount-1);
    }
    Edge& last = geometry->edges.data[index];
    last.polygon=segmentCount;
    last.adjacent=noAdjacent;
    last.end=0;
    last.start=index;
}