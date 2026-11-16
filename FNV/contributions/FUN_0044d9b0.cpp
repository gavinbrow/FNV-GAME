void __cdecl Deallocate(void*);

struct FUN_0044b4b0 {
    virtual ~FUN_0044b4b0();
};
FUN_0044b4b0::~FUN_0044b4b0() {}

struct FUN_0044d9b0 : FUN_0044b4b0 {
    void FUN_00528e40(int);
    void* m04;
    void* m08;
    void* m0c;
    virtual ~FUN_0044d9b0();
};

FUN_0044d9b0::~FUN_0044d9b0() {
    FUN_00528e40(1);
    void* p = m0c;
    Deallocate(p);
    void* q = m04;
    Deallocate(q);
}
