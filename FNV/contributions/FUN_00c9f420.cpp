struct PhysicsAction {
    bool __thiscall FUN_00c68cb0(void* owner);
};
struct LinkedObject {
    PhysicsAction* GetAction() const {
        return *reinterpret_cast<PhysicsAction* const*>(reinterpret_cast<const char*>(this) + 0x350);
    }
};
struct FUN_00c9f420_Class {
    virtual void slot0();
    virtual void slot1();
    virtual void slot2();
    virtual void slot3();
    virtual void slot4();
    virtual void slot5();
    virtual void slot6();
    virtual void slot7();
    virtual void slot8();
    virtual void slot9();
    virtual void slot10();
    virtual void slot11();
    virtual void slot12();
    virtual void slot13();
    virtual void slot14();
    virtual void slot15();
    virtual void slot16();
    virtual void slot17();
    virtual void slot18();
    virtual void slot19();
    virtual void slot20();
    virtual void slot21();
    virtual void slot22();
    virtual void slot23();
    virtual void slot24();
    virtual void slot25();
    virtual void slot26();
    virtual void slot27();
    virtual void slot28();
    virtual void slot29();
    virtual void slot30();
    virtual void slot31();
    virtual void slot32();
    virtual void slot33();
    virtual void slot34();
    virtual void slot35();
    virtual void slot36();
    virtual LinkedObject* ResolveLinkedObject();
    int unk4;
    void* handle;
    bool FUN_00c9f420();
};
bool FUN_00c9f420_Class::FUN_00c9f420()
{
    bool result = false;
    LinkedObject* linked = ResolveLinkedObject();
    PhysicsAction* action = linked ? linked->GetAction() : 0;
    if (action)
        result = action->FUN_00c68cb0(handle);
    return result;
}
