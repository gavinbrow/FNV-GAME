struct FUN_00626630
{
    FUN_00626630();
    ~FUN_00626630();
};

struct FUN_00626560 : public FUN_00626630
{
    void FUN_00626600(int a);
    FUN_00626560(int a);
};

FUN_00626560::FUN_00626560(int a) : FUN_00626630()
{
    FUN_00626600(a);
}
