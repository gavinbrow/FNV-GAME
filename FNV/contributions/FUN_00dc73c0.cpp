struct FUN_00dc92d0_StandIn {
    int FUN_00dc92d0(int, int, int, int);
};

struct FUN_00dc73c0_class {
    void* m0;
    void* m4;
    FUN_00dc92d0_StandIn* m8;
    int FUN_00dc73c0(int a, int b);
};

int FUN_00dc73c0_class::FUN_00dc73c0(int a, int b)
{
    FUN_00dc92d0_StandIn* m = m8;
    *(int*)(b + 4) = 0;
    return m->FUN_00dc92d0(a, 1, 1, b);
}
