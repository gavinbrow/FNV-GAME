
extern void* __cdecl FUN_00aa13e0(unsigned int);
extern void* __cdecl FUN_00a5b690(void*);
extern int DAT_0109b220;
extern unsigned char DAT_011a9594;
typedef long (__stdcall *RefCounter)(volatile long*);
extern RefCounter DAT_00fdf1c0;
extern RefCounter DAT_00fdf1c4;

struct RefCounted {
    virtual void Unused00();
    virtual void DeleteThis();
};

struct FUN_00a5fc10_class {
    void* __thiscall FUN_00a5fc10();
};
struct Texture {
    virtual void DeleteObject(int);
    virtual void Slot01();
    virtual void Slot02();
    virtual void Slot03();
    virtual void Slot04();
    virtual void Slot05();
    virtual void Slot06();
    virtual void Slot07();
    virtual void Slot08();
    virtual void Slot09();
    virtual void Slot10();
    virtual void Slot11();
    virtual void Slot12();
    virtual void Slot13();
    virtual void Slot14();
    virtual void Slot15();
    virtual void Slot16();
    virtual void Slot17();
    virtual void Slot18();
    virtual void Slot19();
    virtual void Slot20();
    virtual void Slot21();
    virtual void Slot22();
    virtual void Slot23();
    virtual void Slot24();
    virtual void Slot25();
    virtual void Slot26();
    virtual void Slot27();
    virtual void Slot28();
    virtual void Slot29();
    virtual void Slot30();
    virtual void Slot31();
    virtual void Slot32();
    virtual void Slot33();
    virtual void Slot34();
    virtual void Slot35();
    virtual void Slot36();
    virtual void Slot37();
    virtual void Slot38();
    virtual void Slot39();
    virtual void Slot40();
    virtual void Slot41();
    virtual void Slot42();
    virtual bool CanPreload();
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    void* m_pOwner;
    void* m_pTarget;
    void* m_pList;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    RefCounted* m_pParent;
};

struct OwnerTriple {
    void* m_pOwner;
    void* m_pTarget;
    void* m_pList;
};

Texture* __cdecl FUN_00a5ff10(RefCounted* parent, void* filename, const OwnerTriple* fields)
{
    void* memory = FUN_00aa13e0(0x48);
    Texture* object = memory ? static_cast<Texture*>(((FUN_00a5fc10_class*)memory)->FUN_00a5fc10()) : 0;
    OwnerTriple* storage = reinterpret_cast<OwnerTriple*>(&object->m_pOwner);
    storage->m_pOwner = fields->m_pOwner;
    storage->m_pTarget = fields->m_pTarget;
    RefCounter release = DAT_00fdf1c4;
    storage->m_pList = fields->m_pList;
    RefCounted* previous = object->m_pParent;
    if (previous != parent) {
        if (previous) {
            if (!release((volatile long*)((char*)previous + 4)))
                previous->DeleteThis();
        }
        object->m_pParent = parent;
        if (parent)
            DAT_00fdf1c0((volatile long*)((char*)parent + 4));
    }
    if (filename) {
        const char* value = (const char*)FUN_00a5b690(filename);
        NiFixedString fixed;
        fixed.m_kHandle = value;
        ((FUN_00a5fba0_class*)object)->FUN_00a5fba0(&fixed);
        if (value != (const char*)DAT_0109b220)
            release((volatile long*)(value - 8));
    }
    if (DAT_011a9594 && !object->CanPreload()) {
        object->DeleteObject(1);
        return 0;
    }
    return object;
}
