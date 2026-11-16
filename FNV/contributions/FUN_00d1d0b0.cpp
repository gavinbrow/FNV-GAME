extern "C" __m128 _mm_set_ps1(float a);
extern "C" __m128 _mm_sub_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_add_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_mul_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_min_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_max_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_andnot_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_or_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_cmpeq_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_cmplt_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_rcp_ps(__m128 a);
extern "C" __m128 _mm_unpackhi_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_shuffle_ps(__m128 a, __m128 b, unsigned int imm);

extern __m128 DAT_010c7170;   // (1,1,1,1)
extern float DAT_01267e30;    // zero vector (bss)
extern __m128 DAT_010cd670;   // HK_REAL_MAX x4

struct VectorMask {
    __m128 bits;
    __forceinline int testX() const { return _mm_movemask_ps(bits) & 1; }
};
struct TreeVector4 {
    __forceinline void operator=(const TreeVector4& other) { m_quad = other.m_quad; }
    __m128 m_quad;
    __forceinline void subtract(const TreeVector4& a, const TreeVector4& b) { m_quad = _mm_sub_ps(a.m_quad,b.m_quad); }
    __forceinline void multiply(const TreeVector4& a) { m_quad = _mm_mul_ps(m_quad,a.m_quad); }
    __forceinline void minimum(const TreeVector4& a, const TreeVector4& b) { m_quad = _mm_min_ps(a.m_quad,b.m_quad); }
    __forceinline void maximum(const TreeVector4& a, const TreeVector4& b) { m_quad = _mm_max_ps(a.m_quad,b.m_quad); }
    __forceinline void broadcastY(const TreeVector4& a) { m_quad = _mm_shuffle_ps(a.m_quad,a.m_quad,0x55); }
    __forceinline void broadcastZ(const TreeVector4& a) { m_quad = _mm_shuffle_ps(a.m_quad,a.m_quad,0xaa); }
    __forceinline VectorMask equal(const TreeVector4& b) const { VectorMask r; r.bits = _mm_cmpeq_ps(m_quad,b.m_quad); return r; }
    __forceinline VectorMask less(const TreeVector4& b) const { VectorMask r; r.bits = _mm_cmplt_ps(m_quad,b.m_quad); return r; }
    __forceinline void choose(const TreeVector4& a, const TreeVector4& b, const VectorMask& m) {
        m_quad = _mm_or_ps(_mm_and_ps(m.bits,b.m_quad),_mm_andnot_ps(m.bits,a.m_quad));
    }
    __forceinline void reciprocal(const TreeVector4& a) {
        __m128 input = _mm_shuffle_ps(a.m_quad,_mm_unpackhi_ps(a.m_quad,DAT_010c7170),0xc4);
        __m128 estimate = _mm_rcp_ps(input);
        m_quad = _mm_sub_ps(_mm_add_ps(estimate,estimate),_mm_mul_ps(_mm_mul_ps(estimate,input),estimate));
    }
};

struct RayQ {
    TreeVector4 m_start;
    TreeVector4 m_invDir;
    __forceinline void init(const TreeVector4& from, const TreeVector4& to) {
        m_start = from;
        TreeVector4 delta; delta.subtract(to, from);
        VectorMask zeros = delta.equal(*reinterpret_cast<const TreeVector4*>(&DAT_01267e30));
        TreeVector4 safe; safe.choose(delta,*reinterpret_cast<const TreeVector4*>(&DAT_010c7170),zeros);
        TreeVector4 inverse; inverse.reciprocal(safe);
        m_invDir.choose(inverse,*reinterpret_cast<const TreeVector4*>(&DAT_010cd670),zeros);
    }
};

struct TreeAabb {
    TreeVector4 m_min;
    TreeVector4 m_max;
    __forceinline int hit(const TreeVector4& start,const TreeVector4& invDir,const TreeVector4& limit) const {
        TreeVector4 lo; lo.subtract(m_min,start);
        lo.multiply(invDir);
        TreeVector4 hi; hi.subtract(m_max,start);
        hi.multiply(invDir);
        TreeVector4 nearT; nearT.minimum(lo,hi);
        TreeVector4 nz; nz.broadcastZ(nearT);
        TreeVector4 nX; nX.maximum(nearT,*reinterpret_cast<const TreeVector4*>(&DAT_01267e30));
        TreeVector4 ny; ny.broadcastY(nearT);
        TreeVector4 farT; farT.maximum(lo,hi);
        TreeVector4 fz; fz.broadcastZ(farT);
        TreeVector4 fX; fX.minimum(farT,limit);
        TreeVector4 nYZ; nYZ.maximum(ny,nz);
        nX.maximum(nX,nYZ);
        TreeVector4 fy; fy.broadcastY(farT);
        TreeVector4 fYZ; fYZ.minimum(fy,fz);
        fX.minimum(fX,fYZ);
        return nX.less(fX).testX();
    }
};

struct TreeNode {
    TreeVector4 m_min;
    TreeVector4 m_max;
    int m_child0;
    int m_child1;
    unsigned int m_parent;
    int m_next;
};

struct TreeNodeArray {
    TreeNode* FUN_00d9a4c0(int index);
};

struct RayVisitor {
    virtual void v00();
    virtual float processLeaf(const TreeNode* node);
};

struct NodeTree {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    TreeNode* m_root;
    int unk14;
    int unk18;
    TreeNodeArray m_nodes;
};

void FUN_00d1d0b0(NodeTree* tree, const TreeVector4* from, const TreeVector4* to, RayVisitor* visitor, float maxFraction)
{
    if (!tree) return;
    TreeNode* node = tree->m_root;
    if (!node) return;

    TreeVector4 fraction;
    fraction.m_quad = _mm_set_ps1(maxFraction);
    RayQ ray;
    ray.init(*from,*to);

    for (;;) {
        TreeAabb bounds;
        bounds = *reinterpret_cast<const TreeAabb*>(&node->m_min);
        TreeNode* next;
        if (node->m_next != 0x7fffffff)
            next = tree->m_nodes.FUN_00d9a4c0(node->m_next);
        else
            next = 0;

        if (bounds.hit(ray.m_start,ray.m_invDir,fraction)) {
            if (!(node->m_parent & 0x80000000)) {
                node = tree->m_nodes.FUN_00d9a4c0(node->m_child0);
                continue;
            }
            float f = visitor->processLeaf(node);
            fraction.m_quad = _mm_set_ps1(f);
        }
        node = next;
        if (!node) break;
    }
}
