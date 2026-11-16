struct Vector4 { int x,y,z,w; };
struct FUN_00d74e20_class {
    void* m_00; void* m_04; char* m_08;
    Vector4 __thiscall FUN_00d74e20();
};
Vector4 FUN_00d74e20_class::FUN_00d74e20() {
    return *reinterpret_cast<const Vector4*>(m_08+0xd0);
}