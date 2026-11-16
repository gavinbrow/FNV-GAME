struct FUN_00c84900_vtbl {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual unsigned int FUN_00c84900_call(unsigned int value);
};
struct FUN_00c84900_object {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    void* field20;
};
extern unsigned char __cdecl FUN_00c84740(void* object, unsigned int value);
unsigned char* __stdcall FUN_00c84900(unsigned char* output, FUN_00c84900_object* object, int unused, FUN_00c84900_vtbl* caller, unsigned int value)
{
    unsigned int result = caller->FUN_00c84900_call(value);
    void* field = object->field20;
    *output = FUN_00c84740(field, result);
    return output;
}