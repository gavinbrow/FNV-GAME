// This implementation incorporates earlier contributors' hash-map identification (2026-10-25).
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct ReferenceObject { virtual void Unknown(); virtual void DeleteThis(); volatile long referenceCount; };
struct ReferencePtr {
    ReferenceObject* object;
    ReferencePtr(const ReferencePtr& other) : object(other.object) {
        if(object) InterlockedIncrement(&object->referenceCount);
    }
};
struct MapEntry { MapEntry* next; unsigned int key; ReferencePtr resource; };
class RendererPacketMap {
public:
    virtual void unknown0();
    virtual unsigned int Bucket(unsigned int key);
    virtual bool Equal(unsigned int a,unsigned int b);
    virtual void Assign(MapEntry* entry,unsigned int key,ReferencePtr value);
    virtual void unknown4();
    virtual MapEntry* CreateEntry();
    unsigned int unknown4_field;
    MapEntry** entries;
    unsigned int count;
    void FUN_00e72cf0(unsigned int key, ReferencePtr value);
};
void RendererPacketMap::FUN_00e72cf0(unsigned int key, ReferencePtr value) {
    unsigned int bucket = Bucket(key);
    MapEntry* entry = entries[bucket];
    for (; entry; entry=entry->next) {
        if (!Equal(key, entry->key)) continue;
        ReferenceObject* previous = entry->resource.object;
        long (__stdcall *dec)(volatile long*) = &InterlockedDecrement;
        if (previous != value.object) {
            if (previous && !dec(&previous->referenceCount))
                previous->DeleteThis();
            entry->resource.object = value.object;
            if (value.object)
                InterlockedIncrement(&value.object->referenceCount);
        }
        if (value.object) {
            ReferenceObject* ptr = value.object;
            if (!dec(&ptr->referenceCount)) ptr->DeleteThis();
        }
        return;
    }
    entry = CreateEntry();
    Assign(entry, key, value);
    entry->next = entries[bucket];
    entries[bucket] = entry;
    ++count;
    if (value.object) {
        ReferenceObject* ptr = value.object;
        if (!InterlockedDecrement(&ptr->referenceCount)) ptr->DeleteThis();
    }
}