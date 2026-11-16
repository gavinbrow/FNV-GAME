struct RefObj { void FUN_00564db0(int); };
struct DispatchMembers {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int field08;
    unsigned int field0c;
    unsigned int unk10;
    unsigned int field14;
    DispatchMembers();
    ~DispatchMembers();
};
struct FloatValue {
    float v;
    FloatValue();
    FloatValue(float);
};
struct SingletonData { unsigned int FUN_009eb620(); };
struct RandomData {
    int FUN_00867d20();
    signed char FUN_00867d60();
    int FUN_00867c60();
};
extern "C" SingletonData DAT_011e0e80;
extern "C" RandomData DAT_011de7b8;
float __cdecl FUN_00435dd0();
struct FUN_009eb500 {
    int field00;
    unsigned int field04;
    RefObj* field08;
    unsigned int field0c;
    bool field10;
    unsigned int field14;
    unsigned int field18;
    DispatchMembers members;
    FloatValue point;
    unsigned int field38;
    FUN_009eb500(unsigned int,RefObj*,unsigned int,unsigned int,unsigned int,unsigned int);
};
FUN_009eb500::FUN_009eb500(unsigned int arg1, RefObj* arg2, unsigned int arg3, unsigned int arg4, unsigned int arg5, unsigned int arg6)
    : members(), point()
{
    field04 = arg1;
    field00 = 0;
    if (arg2) arg2->FUN_00564db0(1);
    field08 = arg2;
    field0c = arg3;
    field10 = false;
    field14 = arg4;
    field18 = arg5;
    members.field08 = arg6;
    members.field0c = DAT_011e0e80.FUN_009eb620();
    field38 = 0;
    members.field14 = (DAT_011de7b8.FUN_00867d20() << 9) | DAT_011de7b8.FUN_00867d60() | (DAT_011de7b8.FUN_00867c60() << 13);
    FloatValue temp(FUN_00435dd0());
    point = temp;
}
