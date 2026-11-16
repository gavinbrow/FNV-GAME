struct Vector4 {
    float x;
    float y;
    float z;
    float w;

    Vector4& FUN_00e531a0(int parameter);
    Vector4 FUN_00e53260(int parameter);
};

Vector4 Vector4::FUN_00e53260(int parameter) {
    Vector4 local = *this;
    return local.FUN_00e531a0(parameter);
}