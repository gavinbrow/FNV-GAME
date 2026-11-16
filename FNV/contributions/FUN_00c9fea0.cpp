struct SphereScaleFields {
    unsigned int m_00, m_04, m_08, m_0c;
    float m_10, m_14, m_18, m_1c;
};
struct SphereScalingMethod : bhkSphereShape {
    void __thiscall FUN_00c9fea0(void* first, ArgB* second);
};
void SphereScalingMethod::FUN_00c9fea0(void* first, ArgB* second) {
    char flag;
    SphereScaleFields* result = reinterpret_cast<SphereScaleFields*>(Target(&flag));
    float scale = second->f10;
    volatile float& initial = result->m_10; result->m_10 = initial * scale;
    result->m_14 *= scale;
    result->m_18 *= scale;
    result->m_1c *= scale;
    FUN_00c84df0(first, second);
}