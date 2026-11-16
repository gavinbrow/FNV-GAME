struct Point2_construct_shell {
    float x, y;
    Point2_construct_shell(float width, float height, const void* axis);
};
struct FUN_004a5ff0_shell : FUN_00c335d0 {
    FUN_004a5ff0_shell(const void* type, const Point2_construct_shell& extent);
};
struct FUN_004a5f50_shell : BGSPrimitive {
    FUN_004a5ff0_shell* FUN_004a5f50();
};
extern int g_011a9448;
extern int g_011f426c;

FUN_004a5ff0_shell* FUN_004a5f50_shell::FUN_004a5f50() {
    return new FUN_004a5ff0_shell(&g_011f426c,
                  Point2_construct_shell(Radii.x, Radii.z, &g_011a9448));
}