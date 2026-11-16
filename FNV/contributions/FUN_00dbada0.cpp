struct Interface
{
    virtual void unk00();
    virtual void unk04();
    virtual void unk08();
    virtual void unk0c();
    virtual void unk10();
    virtual void unk14();
    virtual void unk18();
    virtual void unk1c();
    virtual void unk20();
    virtual void unk24();
    virtual void unk28();
    virtual void unk2c();
    virtual void unk30();
    virtual void unk34();
    virtual void unk38();
    virtual void unk3c();
    virtual void unk40();
    virtual void Invoke(void* value, int argument);
};
struct Wrapper
{
    Interface* interfaceObject;
    void* value;
    void FUN_00dbada0(int argument);
};
void Wrapper::FUN_00dbada0(int argument)
{
    interfaceObject->Invoke(value, argument);
}
