struct FUN_007530a0 {
    virtual ~FUN_007530a0() {}
};

struct FUN_00a7b300 {
    virtual ~FUN_00a7b300() {}
};

struct FUN_00c5ed60 : FUN_00a7b300 {
    int unk04;
    int unk08;
    FUN_007530a0 m_00c;
    virtual ~FUN_00c5ed60();
};

FUN_00c5ed60::~FUN_00c5ed60() {}
