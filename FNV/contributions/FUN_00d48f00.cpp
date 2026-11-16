void* __cdecl FUN_00cb1280(void* destination, int value, int size);
int __cdecl FUN_00cb1290(const void* left, const void* right, int size);
int __cdecl FUN_00cb0fa0(const char* left, const char* right);
const char* __cdecl FUN_00dc0fb0();
int __cdecl FUN_00dc0cd0(void* input, int arg2, int flags);
int __cdecl FUN_00d48d30(void* input, int arg2, int arg3);
extern int DAT_011b7b88;
struct Header180 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    char unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    Header180() {
        FUN_00cb1280(this,-1,64);
        unk00=0x57e0e057;
        unk04=0x10c0c010;
        unk28=0;
    }
};
struct Object180 {
    void* unk00;
    int unk04;
    void* unk08;
    Object180* __thiscall FUN_00dcc6a0(void* input, int arg2);
    void __thiscall FUN_00dcc160();
};
int __cdecl FUN_00d48f00(Header180* input, int arg2, int arg3, int arg4)
{
    Header180 header;
    if (input->unk00==header.unk00 && input->unk04==header.unk04
        && FUN_00cb1290(&input->unk10,&DAT_011b7b88,4)==0
        && FUN_00cb0fa0(&input->unk28,FUN_00dc0fb0())==0)
        return FUN_00dc0cd0(input,arg2,0);
    Object180 object;
    Object180* result=object.FUN_00dcc6a0(input,arg2);
    void* payload = result->unk08;
    int value=FUN_00d48d30(payload,arg3,arg4);
    object.FUN_00dcc160();
    return value;
}
