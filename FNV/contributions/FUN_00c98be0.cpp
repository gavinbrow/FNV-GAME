struct __declspec(align(16)) EC98BE0Vector {
    float x;
    float y;
    float z;
    float w;
    void __thiscall FUN_00c7f7a0(int a, int b);
};
struct EC98BE0Owner {
    void __thiscall FUN_00c98b60(EC98BE0Vector* position, float scalar, int a, int b, int c);
    void __thiscall FUN_00c98be0(int x, int y, float scalar, int a, int b, int c);
};
void EC98BE0Owner::FUN_00c98be0(int x, int y, float scalar, int a, int b, int c)
{
    EC98BE0Vector position;
    position.FUN_00c7f7a0(x, y);
    FUN_00c98b60(&position, scalar, a, b, c);
}