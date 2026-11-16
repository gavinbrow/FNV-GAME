struct FinishLoadedFlag {
    int m_finishing;
};
struct PackedHalf {
    short bits;
    void operator=(float f) {
        int value = *(int*)&f;
        bits = (short)(value >> 16);
    }
};
class FinishableBase {
public:
    FinishableBase(FinishLoadedFlag flag) {
        if (flag.m_finishing) {
            PackedHalf* scale = (PackedHalf*)((char*)this + 0x11e);
            *scale = 1.0f;
        }
    }
    virtual ~FinishableBase() throw();
};
class FUN_00c9d130 : public FinishableBase {
public:
    FUN_00c9d130(FinishLoadedFlag flag) throw();
    virtual ~FUN_00c9d130() throw();
};
FUN_00c9d130::FUN_00c9d130(FinishLoadedFlag flag) throw() : FinishableBase(flag) {}
