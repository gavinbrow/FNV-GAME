extern bool __cdecl FUN_0049e390(float a, float b, float tolerance);

bool __cdecl FUN_0049e2f0(const float* lhs, const float* rhs, float tolerance)
{
    return FUN_0049e390(lhs[0], rhs[0], tolerance)
        && FUN_0049e390(lhs[1], rhs[1], tolerance)
        && FUN_0049e390(lhs[2], rhs[2], tolerance);
}