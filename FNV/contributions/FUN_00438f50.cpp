struct Triple00438f50 {
    int first;
    int second;
    int third;
};

extern Triple00438f50 DAT_011c3ae4;

struct Base00438f50 {
    Base00438f50();
};

struct FUN_00438f50 : Base00438f50 {
    Triple00438f50 values;
    FUN_00438f50();
};

FUN_00438f50::FUN_00438f50()
    : Base00438f50()
{
    values = DAT_011c3ae4;
}