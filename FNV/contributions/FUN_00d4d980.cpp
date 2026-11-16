#include <xmmintrin.h>
extern float DAT_0101e2bc;
extern float DAT_01013ea4;
extern int DAT_010d0994;
struct FUN_00cf4d80_shell { void FUN_00cf4d80(int entityA, int entityB, int name); };
struct FUN_00d4d980_Class : hkpDashpotAction { FUN_00d4d980_Class* FUN_00d4d980(int entityA, int entityB, int name); };
FUN_00d4d980_Class* FUN_00d4d980_Class::FUN_00d4d980(int entityA, int entityB, int name)
{
    reinterpret_cast<FUN_00cf4d80_shell*>(this)->FUN_00cf4d80(entityA, entityB, name);
    m_strength = DAT_0101e2bc;
    m_damping = DAT_01013ea4;
    *reinterpret_cast<int**>(this) = &DAT_010d0994;
    *reinterpret_cast<__m128*>(&m_point[0]) = _mm_setzero_ps();
    *reinterpret_cast<__m128*>(&m_point[1]) = _mm_setzero_ps();
    return this;
}