extern char str_01097164[];
extern int DAT_011f3f68;
extern int __cdecl FUN_00a7d330(int);
extern int __cdecl FUN_00a7d510(char*, int);

struct FUN_0096ad30_param
{
    void* vtable;
    int unk04;
    unsigned short unk08;
    unsigned short unk0A;
    unsigned short unk0C;
    unsigned short unk0E;
    void FUN_0096ad30(unsigned int);
    void FUN_0096ae90(unsigned int, unsigned int*);
};

struct Owner_00a49380
{
    void* vtable;
    int unk04;
    int unk08;
    void FUN_00a5d6e0(FUN_0096ad30_param*);
    void FUN_00a49380(FUN_0096ad30_param*);
};

void Owner_00a49380::FUN_00a49380(FUN_0096ad30_param* param)
{
    unsigned int value;
    unsigned int index;

    FUN_00a5d6e0(param);
    value = FUN_00a7d330(DAT_011f3f68);
    index = param->unk0A;
    if (index >= (unsigned int)param->unk08) {
        param->FUN_0096ad30((unsigned int)param->unk0E + index);
    }
    param->FUN_0096ae90(index, &value);
    value = FUN_00a7d510(str_01097164, unk08);
    index = param->unk0A;
    if (index >= (unsigned int)param->unk08) {
        param->FUN_0096ad30((unsigned int)param->unk0E + index);
    }
    param->FUN_0096ae90(index, &value);
}

