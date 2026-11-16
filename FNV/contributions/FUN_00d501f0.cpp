extern int DAT_01268188;
extern int DAT_01268f74;
extern __declspec(thread) int g_ThreadMemoryContext;
void* __cdecl FUN_00aa13e0(unsigned int size);
void __cdecl FUN_00c876f0();
void __cdecl FUN_00c87700();

struct DataBase
{
    DataBase();
    virtual ~DataBase();
    static void* operator new(unsigned int size) { return FUN_00aa13e0(size); }
};

struct DataIntermediate : DataBase
{
    int unk04;
    int unk08;
    int unk0c;
    DataIntermediate() : unk0c(0) { ++DAT_01268188; }
};

struct DataObject : DataIntermediate
{
    DataObject() { ++DAT_01268f74; }
};

struct MemoryContextScope
{
    int previousContext;
    MemoryContextScope()
    {
        previousContext = g_ThreadMemoryContext;
        g_ThreadMemoryContext = 16;
    }
    ~MemoryContextScope()
    {
        g_ThreadMemoryContext = previousContext;
    }
};

struct DataFactory
{
    void FUN_00c89730(DataObject* object, int id);
    DataObject* FUN_00d501f0(int id);
};

DataObject* DataFactory::FUN_00d501f0(int id)
{
    MemoryContextScope context;
    FUN_00c876f0();
    DataObject* object = new DataObject();
    FUN_00c89730(object, id);
    FUN_00c87700();
    return object;
}