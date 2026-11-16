#include "h_74712c1d3c73.h"
extern __declspec(thread) int DAT_tls_field;
struct MemoryContextGuard {
    int previous;
    MemoryContextGuard() : previous(DAT_tls_field) { DAT_tls_field = 16; }
    ~MemoryContextGuard() { DAT_tls_field = previous; }
};
struct FUN_00c905b0_Class {
    void FUN_00c905b0();
};
struct FUN_00a5d3d0 {
    virtual ~FUN_00a5d3d0();
};
struct FUN_00c87d20 : FUN_00a5d3d0 {
    int m_field04;
    FUN_00c905b0_Class* m_ref;
    virtual ~FUN_00c87d20();
};
FUN_00c87d20::~FUN_00c87d20() {
    MemoryContextGuard guard;
    if (m_ref)
        m_ref->FUN_00c905b0();
}