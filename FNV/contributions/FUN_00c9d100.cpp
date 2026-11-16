extern int DAT_010c59f4;
extern int DAT_010c6bec;

struct MotionStateObject {
    void* volatile m_vtable;
    MotionStateObject* FUN_00c9d100(int enabled);
};

MotionStateObject* MotionStateObject::FUN_00c9d100(int enabled)
{
    m_vtable = &DAT_010c59f4;
    if (enabled != 0) {
        *reinterpret_cast<volatile float*>(&enabled) = 1.0f;
        *reinterpret_cast<unsigned short*>(reinterpret_cast<char*>(this) + 0x11e) =
            static_cast<unsigned short>(enabled >> 16);
    }
    m_vtable = &DAT_010c6bec;
    return this;
}
