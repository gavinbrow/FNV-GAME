struct FastNavMeshVertHandle
{
    FastNavMeshVertHandle& operator=(FastNavMeshVertHandle const&);
};

struct S00691c60
{
    int m0;
    FastNavMeshVertHandle m4;

    S00691c60(S00691c60 const&);
};

struct FUN_00691c10_class
{
    virtual void v0();
    void* m4;

    int FUN_00978bc0();
    void FUN_00692320(int, int);
    int FUN_00691c10(S00691c60 const&);
};

int __thiscall FUN_00691c10_class::FUN_00691c10(S00691c60 const& param_2)
{
    int count = FUN_00978bc0();

    FUN_00692320(count * 12 + reinterpret_cast<int>(m4), 1);

    reinterpret_cast<S00691c60*>(
        reinterpret_cast<int>(m4) + count * 12)->FUN_00691c60(param_2);

    return count;
}