struct NiTMallocInterface_004d91b0 {
    static void __cdecl Deallocate(void*);
};
struct FUN_004d91b0_Class {
    virtual void v00();
    void* pData;
    ~FUN_004d91b0_Class();
};
FUN_004d91b0_Class::~FUN_004d91b0_Class()
{
    NiTMallocInterface_004d91b0::Deallocate(pData);
}
