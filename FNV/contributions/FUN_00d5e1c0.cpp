struct FUN_00d5e1c0_Shape {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void slot10();
    virtual void slot14();
    virtual void slot18();
    virtual void slot1c();
    virtual void slot20();
    virtual void slot24();
    virtual void slot28();
    virtual int GetElementCount();
    virtual void WriteElements(void* destination);
};
struct FUN_00d5e1c0_Collection {
    int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c;
    int unk20,unk24,unk28,unk2c,unk30,unk34,unk38,unk3c;
    int unk40;
    FUN_00d5e1c0_Shape** elements;
    int count;
    void* __thiscall FUN_00d5e1c0(void* destination);
};
void* __thiscall FUN_00d5e1c0_Collection::FUN_00d5e1c0(void* destination)
{
    char* cursor = (char*)destination;
    for (int i=0; i<count; ++i) {
        FUN_00d5e1c0_Shape* element = elements[i];
        element->WriteElements(cursor);
        cursor += element->GetElementCount() * 16;
    }
    return destination;
}