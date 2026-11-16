struct TransformMatrix {
    float m00, m01, m02;
    float m10, m11, m12;
    float m20, m21, m22;
    bool FUN_004d9ae0(const TransformMatrix& other) const;
};
struct TransformPoint {
    float x, y, z;
    bool FUN_00439090(const TransformPoint& other) const;
};
struct Transform3D {
    TransformMatrix rotation;
    TransformPoint translation;
    float scale;
    unsigned int FUN_00a86c30(const Transform3D& other) const;
};
unsigned int Transform3D::FUN_00a86c30(const Transform3D& other) const {
    if (rotation.FUN_004d9ae0(other.rotation)) {
        if (!translation.FUN_00439090(other.translation)) {
            if (scale == other.scale)
                return false;
        }
    }
    return true;
}