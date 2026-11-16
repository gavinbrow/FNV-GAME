
struct CleanupMember_00721920 {
    ~CleanupMember_00721920();
};

struct FUN_00721920 {
    virtual ~FUN_00721920();
    CleanupMember_00721920 cleanup;
    void __thiscall FUN_00721990();
};

void __cdecl FUN_007211c0(void* object);

FUN_00721920::~FUN_00721920() {
    FUN_00721990();
    FUN_007211c0(this);
}
