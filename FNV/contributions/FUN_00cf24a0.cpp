#include <xmmintrin.h>
struct PhantomBounds {
    void __thiscall FUN_00d07ec0(hkAabb* bounds);
    void __thiscall FUN_00cf24a0(const hkAabb& source);
};
void PhantomBounds::FUN_00cf24a0(const hkAabb& source)
{
    hkAabb* target = reinterpret_cast<hkAabb*>(reinterpret_cast<char*>(this) + 0xb0);
    _mm_store_ps(&target->m_min.x, _mm_load_ps(&source.m_min.x));
    _mm_store_ps(&target->m_max.x, _mm_load_ps(&source.m_max.x));
    FUN_00d07ec0(target);
}