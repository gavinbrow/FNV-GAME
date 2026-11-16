extern void* DAT_010c70b4;

struct VectorExtents { float x, y, z, w; };

struct BoxShape {
    void* m_vtable;
    unsigned short m_memSize;
    unsigned short m_referenceCount;
    int m_userData;
    int m_shapeType;
    float m_radius;
    float m_localCenterX;
    float m_localCenterY;
    float m_localCenterZ;
    VectorExtents m_halfExtents;

    BoxShape* FUN_00c9ddb0(const float* extents, float radius);
};

BoxShape* BoxShape::FUN_00c9ddb0(const float* extents, float radius)
{
    m_radius = radius;
    m_referenceCount = 1;
    m_userData = 0;
    m_shapeType = 4;
    m_vtable = &DAT_010c70b4;
    m_halfExtents = *reinterpret_cast<const VectorExtents*>(extents);

    float smaller = m_halfExtents.x < m_halfExtents.y ? m_halfExtents.x : m_halfExtents.y;
    m_halfExtents.w = smaller;
    m_halfExtents.w = m_halfExtents.z < m_halfExtents.w ? m_halfExtents.z : m_halfExtents.w;
    return this;
}
