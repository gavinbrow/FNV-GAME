#include "h_056ae9dde66e.h"
inline void* operator new(unsigned int, void* p) { return p; }
class MotionGravityBase : public hkpKeyframedRigidMotion {
public:
    explicit MotionGravityBase(int initialize) {
        if (initialize) {
            float gravityFactor = 1.0f;
            volatile short& storedGravityFactor = m_gravityFactor;
            storedGravityFactor = static_cast<short>(*reinterpret_cast<int*>(&gravityFactor) >> 16);
        }
    }
};
class KeyframedMotionReset : public MotionGravityBase {
public:
    explicit KeyframedMotionReset(int initialize) : MotionGravityBase(initialize) {}
    KeyframedMotionReset* FUN_00c9d1c0(int initialize);
};
KeyframedMotionReset* KeyframedMotionReset::FUN_00c9d1c0(int initialize) {
    __assume(this != 0);
    new (this) KeyframedMotionReset(initialize);
    return this;
}