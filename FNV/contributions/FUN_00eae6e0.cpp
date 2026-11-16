struct VTableObject {
    virtual void __fastcall Query(int value);
    virtual void __fastcall AddRef(int value);
    virtual void __fastcall Release(int value);
};
void __fastcall FUN_00eae6e0(VTableObject* object, int value)
{
    object->Release(value);
}
