struct Triple {
    int x;
    int y;
    int z;
    Triple() : x(0), y(0), z(0x80000000) {}
};
struct FUN_00dbd870 {
    Triple first;
    Triple second;
    Triple third;
    Triple fourth;
    int trailing;
    FUN_00dbd870();
};
FUN_00dbd870::FUN_00dbd870() : trailing(0)
{
}
