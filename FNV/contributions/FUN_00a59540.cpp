struct Matrix161 {
    float entry[3][3];

    Matrix161* FUN_0043f8d0(Matrix161* result, const Matrix161* other) const;
    void FUN_00a59540(float xAngle, float yAngle, float zAngle);
};

void Matrix161::FUN_00a59540(float xAngle, float yAngle, float zAngle)
{
    Matrix161 rotations[3];
    float sine, cosine;
    fnv_SinCos(xAngle, sine, cosine);

    Matrix161& x = rotations[2];
    x.entry[0][0] = 1.0f;
    x.entry[0][1] = 0.0f;
    x.entry[0][2] = 0.0f;
    x.entry[1][0] = 0.0f;
    x.entry[1][1] = cosine;
    x.entry[1][2] = sine;
    x.entry[2][0] = 0.0f;
    x.entry[2][1] = -sine;
    x.entry[2][2] = cosine;

    fnv_SinCos(yAngle, sine, cosine);

    Matrix161& y = rotations[0];
    y.entry[0][0] = cosine;
    y.entry[0][1] = 0.0f;
    y.entry[0][2] = -sine;
    y.entry[1][0] = 0.0f;
    y.entry[1][1] = 1.0f;
    y.entry[1][2] = 0.0f;
    y.entry[2][0] = sine;
    y.entry[2][1] = 0.0f;
    y.entry[2][2] = cosine;

    fnv_SinCos(zAngle, sine, cosine);

    Matrix161& z = rotations[1];
    z.entry[0][0] = cosine;
    z.entry[0][1] = sine;
    z.entry[0][2] = 0.0f;
    z.entry[1][0] = -sine;
    z.entry[1][1] = cosine;
    z.entry[1][2] = 0.0f;
    z.entry[2][0] = 0.0f;
    z.entry[2][1] = 0.0f;
    z.entry[2][2] = 1.0f;

    Matrix161 temporary;
    Matrix161* yz = y.FUN_0043f8d0(&temporary, &z);
    *this = *x.FUN_0043f8d0(&y, yz);
}
