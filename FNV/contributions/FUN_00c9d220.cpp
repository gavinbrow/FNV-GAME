struct MotionCtorBase : public hkpMotion {
    virtual ~MotionCtorBase();
    MotionCtorBase(int flag) {
        if (flag) {
            *reinterpret_cast<float*>(&flag) = 1.0f;
            volatile short& gravityFactor = m_gravityFactor;
            gravityFactor = static_cast<short>(flag >> 16);
        }
    }
};
struct FUN_00c9d220 : public MotionCtorBase {
    virtual ~FUN_00c9d220();
    FUN_00c9d220(int flag);
};
FUN_00c9d220::FUN_00c9d220(int flag) : MotionCtorBase(flag) {}
