struct Vector4 { float x; float y; float z; float w; };
struct Matrix44;
struct FUN_00cb21e0_shell { void __thiscall FUN_00cb21e0(const Matrix44* source); };
struct FUN_00cb2240_shell { void __thiscall FUN_00cb2240(const Matrix44* left, const Matrix44* right); };
__declspec(align(16)) struct Matrix44 {
    Vector4 row0;
    Vector4 row1;
    Vector4 row2;
    Vector4 row3;
    void FUN_00cb2420(const Matrix44* left, const Matrix44* right);
};
void Matrix44::FUN_00cb2420(const Matrix44* left, const Matrix44* right) {
    Matrix44 temporary;
    ((FUN_00cb21e0_shell*)&temporary)->FUN_00cb21e0(right);
    ((FUN_00cb2240_shell*)this)->FUN_00cb2240(left, &temporary);
}
