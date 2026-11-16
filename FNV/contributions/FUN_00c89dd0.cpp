#include <intrin.h>
extern volatile unsigned long DAT_0126fd98;

struct MemoryCategoryScope_00c89dd0 {
    int previous;
    MemoryCategoryScope_00c89dd0(int* block) : previous(block[0x2b4 / 4]) {
        block[0x2b4 / 4] = 16;
    }
    ~MemoryCategoryScope_00c89dd0() { previous = 0; }
};

struct PendingAllocation_00c89dd0 {
    void* pointer;
    PendingAllocation_00c89dd0(void* value) : pointer(value) {}
    ~PendingAllocation_00c89dd0() { pointer = 0; }
};

struct Allocator_00c89dd0 {
    virtual void reserved();
    virtual void* allocate(unsigned int bytes);
};
SpawnedAllocHolder* FUN_00c85750();

struct CloneData_00c89dd0 {
    int unknown00;
    void* first;
    void* second;
    void* third;
    void* fourth;
};
struct Instance_00c89dd0 {
    Instance_00c89dd0* FUN_00cf3ea0(void* first, void* second, void* third, void* fourth);
};
struct RefCounted_00c89dd0 {
    void FUN_00c905b0();
};
struct Dispatch_00c89dd0 {
    virtual void reserved00();
    virtual void reserved01();
    virtual void reserved02();
    virtual void reserved03();
    virtual void reserved04();
    virtual void reserved05();
    virtual void reserved06();
    virtual void reserved07();
    virtual void reserved08();
    virtual void reserved09();
    virtual void reserved10();
    virtual void reserved11();
    virtual void reserved12();
    virtual void reserved13();
    virtual void reserved14();
    virtual void reserved15();
    virtual void reserved16();
    virtual void reserved17();
    virtual void reserved18();
    virtual void reserved19();
    virtual void reserved20();
    virtual void reserved21();
    virtual void reserved22();
    virtual void reserved23();
    virtual void reserved24();
    virtual void reserved25();
    virtual void reserved26();
    virtual void reserved27();
    virtual void reserved28();
    virtual void reserved29();
    virtual void reserved30();
    virtual void reserved31();
    virtual void reserved32();
    virtual void reserved33();
    virtual void reserved34();
    virtual void attach(Instance_00c89dd0*);
    virtual void reserved36();
    virtual void reserved37();
    virtual void reserved38();
    virtual void reserved39();
    virtual void reserved40();
    virtual void reserved41();
    virtual void reserved42();
    virtual void reserved43();
    virtual void reserved44();
    virtual void reserved45();
    virtual void reserved46();
    virtual void finish(int);
    void FUN_00c89dd0(int data);
};

void Dispatch_00c89dd0::FUN_00c89dd0(int data) {
    Dispatch_00c89dd0* owner = this;
    unsigned int slot = DAT_0126fd98;
    int* block = (int*)((void**)__readfsdword(0x2c))[slot];
    MemoryCategoryScope_00c89dd0 memoryScope(block);
    CloneData_00c89dd0* clone = data ? (CloneData_00c89dd0*)(data - 4) : 0;
    SpawnedAllocHolder* holder = FUN_00c85750();
    Allocator_00c89dd0* allocator = (Allocator_00c89dd0*)holder->m_pAllocator;
    void* memory = allocator->allocate(0x38);
    *(unsigned short*)((char*)memory + 4) = 0x38;
    Instance_00c89dd0* instance;
    {
        PendingAllocation_00c89dd0 pending(memory);
        void* argFourth = clone->fourth;
        void* argFirst = clone->third;
        void* argLast = clone->second;
        void* argThird = clone->first;
        instance = ((Instance_00c89dd0*)memory)->FUN_00cf3ea0(argFirst, argFourth, argThird, argLast);
    }
    owner->attach(instance);
    ((RefCounted_00c89dd0*)instance)->FUN_00c905b0();
    owner->finish(data);
    block[0x2b4 / 4] = memoryScope.previous;
}