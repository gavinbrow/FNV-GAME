static void triangleIndices(unsigned short* indices, int tri, int& a, int& b, int& c) {
    int offset=tri*3; a=indices[offset++]; b=indices[offset++]; c=indices[offset];
}
struct V3 {
    float x, y, z;
    V3() {}
    V3(float a, float b, float c) : x(a), y(b), z(c) {}
    V3 operator+(const V3& b) const { return V3(x+b.x, y+b.y, z+b.z); }
    V3 operator-(const V3& b) const { return V3(x-b.x, y-b.y, z-b.z); }
    V3 operator*(float f) const { return V3(x*f, y*f, z*f); }
    float Dot(const V3& b) const { return x*b.x + y*b.y + z*b.z; }
    static float StaticDot(const V3& a, const V3& b) { return a.x*b.x+a.y*b.y+a.z*b.z; }
    V3& operator=(const V3& b) { x=b.x; y=b.y; z=b.z; return *this; }
    V3& operator+=(const V3& b) { x+=b.x; y+=b.y; z+=b.z; return *this; }
};
struct M3 {
    V3 row0, row1, row2;

};
struct LocalObj
{
    int m_00; int m_04; int m_08; int m_0c; int m_10; int m_14; int m_18; int m_1c; int m_20; int m_24; int m_28; int m_2c; int m_30;
    void FUN_00a86bf0();
};
struct SubObj
{
    int m_00; int m_04; int m_08;
};
struct WorkObj
{
    int m_00; int m_04; int m_08; int m_0c; int m_10; int m_14; int m_18; int m_1c;
    int m_20;
    void FUN_00a59980(void* a1, void* a2);
};
struct RayNodeW7
{
    void* unk00;
    V3 center;
    M3 matrix;
    V3 extent; int unk40; int unk44; int unk48; int unk4c; int unk50;
    int unk54; int unk58; int unk5c; int unk60; int unk64; int unk68; int unk6c; int unk70;
    int unk74; int unk78; int unk7c;
    ChildTest* m_0x80;
    ChildTest* m_0x84;
    int m_0x88;
    void FUN_00eb8ae0(void* out, unsigned short* a1, V3* a2, int a3, int a4, int a5, int a6, int* a7);
    void FUN_00eb94e0(int a0, unsigned short* a1, V3* a2, int a3, int a4, int a5, int a6, int* a7);
};

void RayNodeW7::FUN_00eb94e0(int a0, unsigned short* a1, V3* a2, int a3, int a4, int a5, int a6, int* a7)
{
    V3& origin = center;
    M3& mat = matrix;
    float* entries = (float*)&matrix;
    SubObj sub;
    WorkObj work;
    LocalObj detail;
    FUN_00eb8ae0(&work, a1, a2, a3, a4, a5, a6, a7);
    work.FUN_00a59980(&sub, &mat);
    V3 lower(0,0,0), upper(0,0,0);
    unsigned short index = (unsigned short)a5;
    if ((int)(unsigned short)index <= a6) {
        do {
            int first,second,third;
            triangleIndices(a1,a7[(unsigned short)index],first,second,third);
            const V3* p0 = &a2[first];
            const V3* p1 = &a2[second];
            const V3* p2 = &a2[third];
            V3 d0,d1,d2;
            float t0,t1,t2;
            d0= *p0 - origin;
            t0 = d0.x*entries[0] + d0.y*entries[1] + d0.z*entries[2];
            t1 = d0.Dot(mat.row1);
            t2 = d0.x*entries[6] + d0.y*entries[7] + d0.z*entries[8];

            if (t0 < lower.x) lower.x = t0; else if (t0 > upper.x) upper.x = t0;
            if (t1 < lower.y) lower.y = t1; else if (t1 > upper.y) upper.y = t1;
            if (t2 < lower.z) lower.z = t2; else if (t2 > upper.z) upper.z = t2;
            d1= *p1 - origin;
            t0 = d1.x*entries[0] + d1.y*entries[1] + d1.z*entries[2];
            t1 = d1.Dot(mat.row1);
            t2 = d1.x*entries[6] + d1.y*entries[7] + d1.z*entries[8];

            if (t0 < lower.x) lower.x = t0; else if (t0 > upper.x) upper.x = t0;
            if (t1 < lower.y) lower.y = t1; else if (t1 > upper.y) upper.y = t1;
            if (t2 < lower.z) lower.z = t2; else if (t2 > upper.z) upper.z = t2;
            d2= *p2 - origin;
            t0 = d2.x*entries[0] + d2.y*entries[1] + d2.z*entries[2];
            t1 = d2.Dot(mat.row1);
            t2 = d2.x*entries[6] + d2.y*entries[7] + d2.z*entries[8];

            if (t0 < lower.x) lower.x = t0; else if (t0 > upper.x) upper.x = t0;
            if (t1 < lower.y) lower.y = t1; else if (t1 > upper.y) upper.y = t1;
            if (t2 < lower.z) lower.z = t2; else if (t2 > upper.z) upper.z = t2;
            ++index;
        } while ((int)(unsigned short)index <= a6);
    }
    extent = (upper-lower)*0.5;
    V3 midpoint = (upper+lower)*0.5;
    origin += mat.row0*midpoint.x + mat.row1*midpoint.y + mat.row2*midpoint.z;
    detail.FUN_00a86bf0();
    ((QueryContext*)&origin)->FUN_00eba480(&detail);
    unk7c = a0;
}
