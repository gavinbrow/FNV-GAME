void __cdecl FUN_00d38130(void*, void*, void*, void*);
struct D38AC0Data {
    int unk00;
    char unk04;
    char unk05;
    char unk06;
    char unk07;
    int unk08;
};
void __cdecl FUN_00d38ac0(void* first, void* second, void* third, int fourth)
{
    D38AC0Data data;
    data.unk08 = fourth;
    data.unk04 = 0;
    data.unk00 = 0x10ce81c;
    FUN_00d38130(second, first, third, &data);
}
