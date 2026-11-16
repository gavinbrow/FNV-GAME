inline void* __cdecl operator new(unsigned int, void* p) { return p; }
void* __cdecl FUN_00c85750();

struct AllocationManager {
    virtual void* GetHeap();
    virtual void* Allocate(unsigned int size);
};

struct GlobalOwner {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    AllocationManager* allocator;
};

struct hkpBvTreeStreamAgent {
    virtual void Destroy();
    unsigned short unk04;
    hkpBvTreeStreamAgent(void* a, void* b, void* c, void* d);
};

template <class Agent>
struct hkpSymmetricAgent : Agent {
    hkpSymmetricAgent(void* a, void* b, void* c, void* d)
        : Agent(b, a, c, d) {}
    virtual void Destroy();
};

hkpSymmetricAgent<hkpBvTreeStreamAgent>* __cdecl FUN_00d2e680(void* a, void* b, void* c, void* d)
{
    GlobalOwner* owner = (GlobalOwner*)FUN_00c85750();
    void* object = owner->allocator->Allocate(0x40);
    *(unsigned short*)((char*)object + 4) = 0x40;
    return new (object) hkpSymmetricAgent<hkpBvTreeStreamAgent>(a, b, c, d);
}



