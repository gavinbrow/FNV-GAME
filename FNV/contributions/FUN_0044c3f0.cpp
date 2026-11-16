
struct BaseInterface {
    virtual void Interface();
    void FUN_0044b4b0();
    ~BaseInterface() { FUN_0044b4b0(); }
};
struct FUN_0044c3f0 : BaseInterface {
    void* first;
    void* unused;
    void* second;
    void FUN_0044c480(int flag);
    ~FUN_0044c3f0();
};
FUN_0044c3f0::~FUN_0044c3f0() {
    FUN_0044c480(1);
    void* savedSecond = second;
    ::operator delete(savedSecond);
    void* savedFirst = first;
    ::operator delete(savedFirst);
}
