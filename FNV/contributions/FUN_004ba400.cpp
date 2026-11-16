void _Deallocate(void*);

struct FUN_0045cec0 {
    ~FUN_0045cec0();
};

struct FUN_004b9e50 {
    virtual ~FUN_004b9e50();
};

struct FUN_004ba400 : FUN_004b9e50 {
    int unk04;
    int unk08;
    int unk0c;
    void* m_10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    FUN_0045cec0 m_24;

    void FUN_004ba600();
    void FUN_004baec0();

    virtual ~FUN_004ba400();
};

FUN_004ba400::~FUN_004ba400() {
    FUN_004ba600();
    FUN_004baec0();
    void* p = m_10;
    _Deallocate(p);
}
