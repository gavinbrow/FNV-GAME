struct MotorAllocator {
    virtual void Release(void*);
    virtual void* Allocate(unsigned int size);
};
struct MemoryRouter {
    void* m_context;
    void* m_activeThread;
    void* m_allocatorContext;
    void* m_debugData;
    MotorAllocator* m_allocator;
};
MemoryRouter* __cdecl FUN_00c85750();
extern int DAT_010cb76c;
extern int DAT_010cb780;
extern int DAT_010cb798;
struct ReferencedMotorView {
    void* m_vtable;
    unsigned short m_memorySizeAndFlags;
    short m_referenceCount;
};
struct ConstraintMotorView {
    void* volatile m_vtable;
    unsigned short m_memorySizeAndFlags;
    short m_referenceCount;
    unsigned char m_motorType;
};
struct PositionConstraintMotor {
    void* m_vtable;
    unsigned short m_memorySizeAndFlags;
    short m_referenceCount;
    unsigned char m_motorType;
    unsigned char m_reserved09;
    unsigned char m_reserved0A;
    unsigned char m_reserved0B;
    float m_minForce;
    float m_maxForce;
    float m_tau;
    float m_damping;
    float m_proportionalRecoveryVelocity;
    float m_constantRecoveryVelocity;
    PositionConstraintMotor* __thiscall FUN_00cdf5b0();
};
PositionConstraintMotor* __thiscall PositionConstraintMotor::FUN_00cdf5b0()
{
    MemoryRouter* router = FUN_00c85750();
    PositionConstraintMotor* copy = (PositionConstraintMotor*)router->m_allocator->Allocate(0x24);
    ReferencedMotorView* referenced = (ReferencedMotorView*)copy;
    referenced->m_vtable = &DAT_010cb76c;
    referenced->m_memorySizeAndFlags = 0x24;
    referenced->m_referenceCount = 1;
    const unsigned char motorType = m_motorType;
    ConstraintMotorView* motor = (ConstraintMotorView*)copy;
    motor->m_vtable = &DAT_010cb780;
    motor->m_motorType = motorType;
    copy->m_minForce = m_minForce;
    copy->m_maxForce = m_maxForce;
    copy->m_vtable = &DAT_010cb798;
    copy->m_tau = m_tau;
    copy->m_damping = m_damping;
    copy->m_proportionalRecoveryVelocity = m_proportionalRecoveryVelocity;
    copy->m_constantRecoveryVelocity = m_constantRecoveryVelocity;
    return copy;
}