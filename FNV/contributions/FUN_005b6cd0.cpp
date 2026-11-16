struct FNV_5b6cd0_Data {
    unsigned int field00;
    unsigned char field04;
    unsigned char field05;
    unsigned short field06;
    unsigned int field08;
};
void __cdecl FUN_00878160(FNV_5b6cd0_Data*, int, int, int);
void __cdecl FUN_00878250(unsigned int);
void __cdecl FUN_00878200(FNV_5b6cd0_Data*);
struct FNV_5b6cd0_Host {
    void FUN_004539a0(int, int);
};
extern FNV_5b6cd0_Host* DAT_011dea10;
bool __cdecl FUN_005b6cd0() {
    FNV_5b6cd0_Data data;
    FUN_00878160(&data, 1, 1, 1);
    DAT_011dea10->FUN_004539a0(1, 0);
    FUN_00878250(data.field05);
    FUN_00878200(&data);
    return true;
}