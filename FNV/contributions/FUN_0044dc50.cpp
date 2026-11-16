void __cdecl FUN_00401030(void* apMemory);
struct FUN_0044dc50 : FUN_0044b4b0 {
    void* m_04;
    void* m_08;
    void* m_0c;
    void FUN_00528e40(int aiFlag);
    virtual ~FUN_0044dc50();
};
FUN_0044dc50::~FUN_0044dc50()
{
    void* pkTail;
    void* pkHead;
    FUN_00528e40(1);
    pkHead = m_0c;
    FUN_00401030(pkHead);
    pkTail = m_04;
    FUN_00401030(pkTail);
}
