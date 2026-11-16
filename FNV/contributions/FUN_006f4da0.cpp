struct FUN_006dcbb0 : public PathingLocation {
    FUN_006dcbb0();
    ~FUN_006dcbb0();
    void FUN_006dcce0(int);
    bool FUN_006dd6f0(int);
};

struct FUN_006f4da0 {
    unsigned int flags;
    FUN_006dcbb0 path;
    int context;
    FUN_006f4da0(int, int);
};

FUN_006f4da0::FUN_006f4da0(int source, int contextValue)
    : path()
{
    path.FUN_006dcce0(source);
    context = contextValue;
    flags = 6;
    if (path.FUN_006dd6f0(0))
        flags |= 1;
}