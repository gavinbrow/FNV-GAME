struct FUN_00438af0_t {
    void FUN_00438af0();
};

struct FUN_004edb30 {
    virtual ~FUN_004edb30();
};

struct FUN_004edad0 : FUN_004edb30 {
    virtual ~FUN_004edad0();
};

FUN_004edad0::~FUN_004edad0()
{
    reinterpret_cast<FUN_00438af0_t*>(this)->FUN_00438af0();
}
