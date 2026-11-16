extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long*);
void* __cdecl FUN_00aa13e0(unsigned int);
char* __cdecl FUN_00a5b690(const char*);
void __cdecl FUN_00aa10f0(void*);
void* __cdecl FUN_00aa1070(unsigned int);
void* __cdecl FUN_00ec44d0(void*, const void*, unsigned int);
extern char* EmptyFS;
extern unsigned int DAT_011f5fc4[];
inline void* operator new(unsigned int, void* location) { return location; }

struct FUN_00e81ba0 {
    virtual ~FUN_00e81ba0();
    unsigned int referenceCount;
    unsigned int unk08;
    char* shaderName;
    unsigned int unk10;
    unsigned int flags;
    unsigned int parameter;
    unsigned int additionalValue;
    unsigned int registerType;
    char* propertyName;
    unsigned int elementSize;
    int elementType;
    void* data;
    bool ownsData;
    FUN_00e81ba0();
};

template <class T> struct ShaderPointer { T* p; };
template <class T> struct ShaderArray {
    void* owner;
    T* data;
    unsigned short capacity;
    unsigned short size;
    unsigned short count;
    unsigned short grow;
};
struct ShaderConstantMap_83650 {
    virtual void vfn_0();
    virtual void vfn_4();
    virtual void vfn_8();
    virtual void vfn_c();
    virtual void vfn_10();
    virtual void vfn_14();
    virtual void vfn_18();
    virtual void vfn_1c();
    virtual void vfn_20();
    virtual void vfn_24();
    virtual void vfn_28();
    virtual void vfn_2c();
    virtual void vfn_30();
    virtual void vfn_34();
    virtual void vfn_38();
    virtual void vfn_3c();
    virtual void vfn_40();
    virtual void vfn_44();
    virtual void vfn_48();
    virtual void vfn_4c();
    virtual void vfn_50();
    virtual void vfn_54();
    virtual void vfn_58();
    virtual void vfn_5c();
    virtual void vfn_60();
    virtual void vfn_64();
    virtual void vfn_68();
    virtual void vfn_6c();
    virtual void vfn_70();
    virtual void vfn_74();
    virtual void vfn_78();
    virtual void vfn_7c();
    virtual int vfn_80(FUN_00e81ba0*);
    unsigned int unk04;
    int renderStage;
    ShaderArray<ShaderPointer<FUN_00e81ba0> > entries;
    ShaderArray<ShaderPointer<FUN_00e81ba0> > defined;
    bool modified;
    char pad2d[3];
    void* last;
    unsigned int error;
    unsigned int FUN_00e83650(const char* shader, unsigned int flags, unsigned int parameter,
        unsigned int additionalValue, unsigned int registerType, const char* property,
        unsigned int elementSize, int elementType, void* data, bool copied);
};

unsigned int ShaderConstantMap_83650::FUN_00e83650(const char* shader, unsigned int flags,
    unsigned int parameter, unsigned int additionalValue, unsigned int registerType,
    const char* property, unsigned int elementSize, int elementType, void* data, bool copied)
{
    void* memory = FUN_00aa13e0(sizeof(FUN_00e81ba0));
    FUN_00e81ba0* entry = memory ? new(memory) FUN_00e81ba0() : 0;
    char* name;
    if (!shader) name = EmptyFS;
    else name = FUN_00a5b690(shader);
    if (entry->shaderName != name) {
        if (name != EmptyFS)
            InterlockedIncrement((long*)(name - 8));
        if (entry->shaderName != EmptyFS)
            InterlockedDecrement((long*)(entry->shaderName - 8));
        entry->shaderName = name;
    }
    if (name != EmptyFS)
        InterlockedDecrement((long*)(name - 8));

    flags = (flags & 0x0fffffff) | 0x10000000;
    if (elementSize == 8) flags |= 5;
    else if (elementSize == 12) flags |= 6;
    else if (elementSize == 16) flags |= 7;
    else if (elementSize == 32) flags |= 9;
    else if (elementSize == 36) flags |= 8;
    else if (elementSize == 48) flags |= 9;
    else if (elementSize == 64) flags |= 9;
    entry->flags = flags;

    if (!(elementSize & 3) && elementType == 4 &&
        DAT_011f5fc4[flags & 255] != 1 && DAT_011f5fc4[flags & 255] != 3) {
        if (renderStage == 0) parameter = elementType - 3;
        else if (renderStage == 2) parameter = 2;
    }
    entry->parameter = parameter;
    entry->additionalValue = additionalValue;
    entry->registerType = registerType;

    char* prop;
    if (!property) prop = EmptyFS;
    else prop = FUN_00a5b690(property);
    if (entry->propertyName != prop) {
        if (prop != EmptyFS)
            InterlockedIncrement((long*)(prop - 8));
        if (entry->propertyName != EmptyFS)
            InterlockedDecrement((long*)(entry->propertyName - 8));
        entry->propertyName = prop;
    }
    if (prop != EmptyFS)
        InterlockedDecrement((long*)(prop - 8));

    entry->elementType = elementType;
    entry->elementSize = elementSize;
    if (copied) {
        entry->ownsData = true;
        FUN_00aa10f0(entry->data);
        entry->data = FUN_00aa1070(elementSize);
        FUN_00ec44d0(entry->data, data, elementSize);
    } else {
        entry->ownsData = false;
        entry->data = data;
    }
    error = vfn_80(entry);
    if (error) delete entry;
    return error;
}