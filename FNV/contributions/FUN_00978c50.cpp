struct FUN_00978ea0 {
    virtual ~FUN_00978ea0();
    FUN_00978ea0();
    int m_owner;
    int m_count;
    void* m_data;
};

struct Global_00aa42e0 {
    unsigned int FUN_00aa42e0();
};
Global_00aa42e0* __cdecl FUN_00401020();

struct FUN_00978c50 : FUN_00978ea0 {
    unsigned int m_resource;
    FUN_00978c50();
    virtual ~FUN_00978c50();
    void FUN_006b3f40(unsigned int, unsigned int);
};
FUN_00978c50::FUN_00978c50()
    : FUN_00978ea0()
{
    m_resource = FUN_00401020()->FUN_00aa42e0();
    FUN_006b3f40(0, 0);
}