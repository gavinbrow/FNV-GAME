extern "C" __declspec(thread) int g_memoryContext;

struct Allocator {
    virtual void Release();
    virtual void* Allocate(unsigned int size);
};

struct MemorySystem {
    int m_00;
    int m_04;
    int m_08;
    int m_0c;
    Allocator* allocator;

    void* Allocate(unsigned int bytes) {
        return allocator->Allocate(bytes);
    }
};

extern "C" MemorySystem* __cdecl FUN_00c85750();

struct FUN_00d4edc0 {
    FUN_00d4edc0();
    static void* operator new(unsigned int size) {
        void* memory = FUN_00c85750()->Allocate(0x160);
        *reinterpret_cast<unsigned short*>(
            static_cast<char*>(memory) + 4) = 0x160;
        return memory;
    }
};

struct AllocationContext {
    int previous;
    AllocationContext() {
        previous = g_memoryContext;
        g_memoryContext = 0x10;
    }
    ~AllocationContext() {
        g_memoryContext = previous;
    }
};

struct ObjectHolder {
    int m_00;
    FUN_00d4edc0* object;
    int FUN_00cc5340();
};

int ObjectHolder::FUN_00cc5340() {
    AllocationContext context;
    if (object == 0) {
        object = new FUN_00d4edc0();
    }
    return 0x160;
}