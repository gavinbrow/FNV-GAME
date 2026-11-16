
struct Vec3 { float x, y, z; };
static __forceinline Vec3 sumVec(const Vec3& a, const Vec3& b) {
    Vec3 r; r.x = a.x + b.x; r.y = a.y + b.y; r.z = a.z + b.z; return r;
}
static __forceinline Vec3 diffVec(const Vec3& a, const Vec3& b) {
    Vec3 r; r.x = a.x - b.x; r.y = a.y - b.y; r.z = a.z - b.z; return r;
}
static __forceinline Vec3 sumVecB(const Vec3& a, const Vec3& b) { Vec3 r; const volatile float& first=a.x; r.x=first+b.x; r.y=a.y+b.y; r.z=a.z+b.z; return r; }
struct Triangle3 { Vec3 origin, edge0, edge1; };
struct Segment3 { Vec3 origin, direction; };
extern float __cdecl FUN_00eaff20(const Segment3*, const Triangle3*, float*, float*, float*);
extern float __cdecl FUN_00eb1d20(const Segment3*, const Triangle3*, float*, float*, float*);
float __cdecl FUN_00eb3230(const Triangle3* a, const Triangle3* b,
                            float* aU, float* aV, float* bU, float* bV)
{
    Segment3 edge;
    edge.origin = a->origin;
    edge.direction = a->edge0;
    float best = FUN_00eaff20(&edge, b, aU, bU, bV);
    *aV = 0.0f;

    float av, au;
    struct Pair { float bv, bu; } bc;
    edge.direction = a->edge1;
    float candidate = FUN_00eaff20(&edge, b, &av, &bc.bu, &bc.bv);
    au = 0.0f;
    if (candidate < best) {
        best = candidate;
        *aU = au;
        *aV = av;
        *bU = bc.bu;
        *bV = bc.bv;
    }
    edge.origin = sumVec(a->edge0, edge.origin);
    edge.direction = diffVec(edge.direction, a->edge0);
    candidate = FUN_00eaff20(&edge, b, &av, &bc.bu, &bc.bv);
    au = 1.0f - av;
    if (candidate < best) {
        best = candidate;
        *aU = au;
        *aV = av;
        *bU = bc.bu;
        *bV = bc.bv;
    }

    edge.origin = b->origin;
    edge.direction = b->edge0;
    candidate = FUN_00eb1d20(&edge, a, &bc.bu, &au, &av);
    bc.bv = 0.0f;
    if (candidate < best) {
        best = candidate;
        *aU = au;
        *aV = av;
        *bU = bc.bu;
        *bV = bc.bv;
    }
    edge.direction = b->edge1;
    candidate = FUN_00eb1d20(&edge, a, &bc.bv, &au, &av);
    bc.bu = 0.0f;
    if (candidate < best) {
        best = candidate;
        *aU = au;
        *aV = av;
        *bU = bc.bu;
        *bV = bc.bv;
    }
    edge.origin = sumVecB(b->edge1, b->origin);
    edge.direction = b->edge0;
    candidate = FUN_00eb1d20(&edge, a, &bc.bu, &au, &av);
    bc.bv = 1.0f;
    if (candidate < best) {
        best = candidate;
        *aU = au;
        *aV = av;
        *bU = bc.bu;
        *bV = bc.bv;
    }
    edge.origin = sumVec(b->origin, b->edge0);
    edge.direction = b->edge1;
    candidate = FUN_00eb1d20(&edge, a, &bc.bv, &au, &av);
    if (candidate < best) {
        best = candidate;
        *aU = au;
        *aV = av;
        *bU = 1.0f;
        *bV = bc.bv;
    }
    return best;
}