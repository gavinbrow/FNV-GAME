#include <xmmintrin.h>
void* __cdecl FUN_00ec44d0(void*, const void*, unsigned);
void* __cdecl FUN_00aa13e0(unsigned);
void __cdecl FreeStorage(void*);
struct MemoryManager { void* Allocate(unsigned); };
extern MemoryManager _g_memoryManager;
inline void* operator new[](unsigned size) { return _g_memoryManager.Allocate(size); }
extern __declspec(thread) int g_tlsMemContext;
struct Context {
    int old;
    Context() { old=g_tlsMemContext; g_tlsMemContext=16; }
    ~Context() { g_tlsMemContext=old; }
};
struct Vec3 { float x,y,z; };
struct Triangle { unsigned short a,b,c,unk06; };
struct Region { unsigned value; unsigned count; unsigned other; };
struct Geometry {
    unsigned unk00,unk04;
    unsigned short triangleCount,unk0A,unk0C,unk0E,regionCount,unk12;
    Triangle* triangles;
    Vec3* vertices;
    unsigned unk1C,unk20;
    Region* regions;
    __forceinline bool GetTriangle(unsigned short index,Triangle*& out) {
        out=&triangles[index];
        return index>=triangleCount;
    }
};
struct Input {
    unsigned unk00;
    Geometry* geometry;
    float scale;
    unsigned unk0C;
    __m128 transform;
};
struct MeshPart {
    unsigned vertexCount;
    Vec3* vertices;
    unsigned triangleCount;
    unsigned short* indices;
    struct Bounds* bounds;
    MeshPart();
    ~MeshPart();
};
struct Bounds { unsigned first,second; __forceinline void Init(unsigned a,unsigned b) { first=a;second=b; } };
struct GeometryBase {
    GeometryBase();
    virtual ~GeometryBase();
    unsigned references;
};
struct Mesh : GeometryBase {
    unsigned count;
    MeshPart* parts;
    static void* operator new(unsigned n) { return FUN_00aa13e0(n); }
    Mesh() : count(0), parts(0) {}
    virtual ~Mesh();
};
extern void* indexVtable[];
struct IndexArray {
    void** vtable;
    ~IndexArray() { FreeStorage(data); }
    unsigned short* data;
    unsigned short capacity,size,used,grow;
    IndexArray() { capacity=0; grow=1; size=0; used=0; data=0; vtable=indexVtable; }
    void Resize(unsigned);
    __forceinline void Append(unsigned short value) { SetAt(size,value); }
    __forceinline void SetAt(unsigned index,unsigned short value) {
        if(index>=capacity) Resize(index+grow);
        if(index>=size) {
            size=index+1;
            if(value) ++used;
        } else if(value) {
            if(!data[index]) ++used;
        } else {
            if(data[index]) --used;
        }
        data[index]=value;
    }
    void Clear() {
        unsigned short* values=data;
        unsigned short count=size;
        for(unsigned short index=0;index<count;++index) values[index]=0;
        size=0; used=0;
    }
};
struct Result {
    Mesh* mesh;
    unsigned unk04;
    float scale;
    unsigned unk0C;
    __m128 transform;
    Result(Mesh*);
    ~Result();
};
struct Builder {
virtual void Slot00();
virtual void Slot04();
virtual void Slot08();
virtual void Slot0C();
virtual void Slot10();
virtual void Slot14();
virtual void Slot18();
virtual void Slot1C();
virtual void Slot20();
virtual void Slot24();
virtual void Slot28();
virtual void Slot2C();
virtual void Slot30();
virtual void Slot34();
virtual void Slot38();
virtual void Slot3C();
virtual void Slot40();
virtual void Slot44();
virtual void Slot48();
virtual void Slot4C();
virtual void Slot50();
virtual void Slot54();
virtual void Slot58();
virtual void Slot5C();
virtual void Slot60();
virtual void Slot64();
virtual void Slot68();
virtual void Slot6C();
virtual void Slot70();
virtual void Slot74();
virtual void Slot78();
virtual void Slot7C();
virtual void Slot80();
virtual void Slot84();
virtual void Slot88();
virtual void Slot8C();
virtual void Slot90();
virtual void Slot94();
virtual void Slot98();
virtual void Slot9C();
virtual void SlotA0();
virtual void SlotA4();
virtual void SlotA8();
virtual void SlotAC();
    virtual void Apply(Result*);
    void FUN_00ccc980(Input*);
};
void Builder::FUN_00ccc980(Input* input) {
    Context context;
    Geometry* geometry=input->geometry;
    unsigned short baseVertex=0;
    unsigned short triangleIndex=0;
    Mesh* mesh=new Mesh;
    MeshPart* parts=new MeshPart[geometry->regionCount];
    mesh->parts=parts;
    mesh->count=geometry->regionCount;
    IndexArray indices;
    for(int regionIndex=0;regionIndex<geometry->regionCount;++regionIndex) {
        unsigned triangleCount=0;
        Region* region=&geometry->regions[regionIndex];
        bool done=false;
        while(!done) {
            Triangle* triangle;
            done=geometry->GetTriangle((unsigned short)triangleIndex,triangle);
            if(done) break;
            if(triangle->a >= (unsigned short)baseVertex+region->count) break;
            unsigned short a=triangle->a,b=triangle->b,c=triangle->c;
            indices.Append((unsigned short)(a-baseVertex));
            indices.Append((unsigned short)(b-baseVertex));
            indices.Append((unsigned short)(c-baseVertex));
            ++triangleIndex;
            ++triangleCount;
        }
        unsigned short vertexCount=0;
        if(0 < triangleCount) {
            vertexCount=(unsigned short)region->count;
            Vec3* vertices;
            vertices = (Vec3*)new float[3*(vertexCount+1)];
            for(unsigned short vertex=(unsigned short)baseVertex;
                vertex<(unsigned short)baseVertex+vertexCount;++vertex) {
                vertices[vertex-(unsigned short)baseVertex].x=geometry->vertices[vertex].x;
                vertices[vertex-(unsigned short)baseVertex].y=geometry->vertices[vertex].y;
                vertices[vertex-(unsigned short)baseVertex].z=geometry->vertices[vertex].z;
            }
            unsigned short* copiedIndices=new unsigned short[indices.size];
            unsigned byteCount=2*indices.size;
            FUN_00ec44d0(copiedIndices,indices.data,byteCount);
            void* allocation=_g_memoryManager.Allocate(24);
            unsigned char adj=(unsigned char)(16-((unsigned)allocation&15));
            unsigned adjustment=(unsigned char)adj;
            ((unsigned char*)allocation)[adjustment-1] = adj;
            unsigned char* aligned=(unsigned char*)allocation+adjustment;
            Bounds* bounds=(Bounds*)aligned;
            bounds->Init(geometry->regions[regionIndex].value,geometry->regions[regionIndex].other);
            MeshPart& part=parts[regionIndex];
            part.bounds=bounds;
            part.vertexCount=vertexCount;
            part.vertices=vertices;
            part.indices=copiedIndices;
            part.triangleCount=triangleCount;
        } else {
            --mesh->count;
        }
        indices.Clear();
        baseVertex+=vertexCount;
    }
    Result result(mesh);
    result.scale=input->scale;
    result.transform=input->transform;
    Apply(&result);
}

void* __cdecl NiMalloc(unsigned);
__declspec(noinline) void IndexArray::Resize(unsigned requested) {
    if(requested==capacity) return;
    if(requested<size) {
        for(unsigned short i=(unsigned short)requested;i<size;++i) {
            if(data[i]) {data[i]=0;--used;}
        }
        size=(unsigned short)requested;
    }
    unsigned short* old=data;
    capacity=(unsigned short)requested;
    if(requested>0) {
        data=(unsigned short*)NiMalloc((unsigned short)requested*2);
        for(unsigned short i=0;i<size;++i) data[i]=old[i];
        for(unsigned short i=size;i<capacity;++i) data[i]=0;
    } else data=0;
    FreeStorage(old);
}
