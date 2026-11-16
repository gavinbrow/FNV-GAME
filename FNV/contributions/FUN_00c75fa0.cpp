// Adapted from another contributor's unverified destructor hypothesis and
// adjusted to a single polymorphic primary base, then rechecked by luna1300_133.
void __cdecl FUN_00aa10f0(void* p);

struct PrimaryBase
{
    int m_04;
    void* m_08;
    void Reset();
    virtual ~PrimaryBase();
};

struct FUN_00c75fa0_cls : public PrimaryBase
{
    virtual ~FUN_00c75fa0_cls();
};

PrimaryBase::~PrimaryBase()
{
    this->Reset();
    FUN_00aa10f0(m_08);
}

FUN_00c75fa0_cls::~FUN_00c75fa0_cls()
{
    this->Reset();
}
