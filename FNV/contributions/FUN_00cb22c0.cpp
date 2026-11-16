struct Matrix43;
struct Transform
{
    void FUN_00ce5300(Matrix43* out);
};
struct __declspec(align(16)) Matrix43
{
    float m00, m01, m02, m03;
    float m10, m11, m12, m13;
    float m20, m21, m22, m23;
    float m30, m31, m32, m33;
    void FUN_00cb2240(Matrix43* a, Matrix43* b);
    void FUN_00cb22c0(Transform* a, Matrix43* b);
};
void Matrix43::FUN_00cb22c0(Transform* a, Matrix43* b)
{
    Matrix43 temp;
    a->FUN_00ce5300(&temp);
    this->FUN_00cb2240(&temp, b);
}


