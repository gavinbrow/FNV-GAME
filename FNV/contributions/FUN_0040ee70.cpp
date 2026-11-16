struct FUN_0040ecb0 {
    virtual ~FUN_0040ecb0();
    unsigned char cEtype;
    unsigned char pad05;
    unsigned char pad06;
    unsigned char pad07;
    FUN_0040ecb0* pNext;
};
struct FUN_0045cec0 {
    void* pObject;
    void FUN_0066b0d0(unsigned int);
    ~FUN_0045cec0();
};
struct FUN_0040ee70 : FUN_0040ecb0 {
    FUN_0045cec0 first;
    FUN_0045cec0 second;
    virtual ~FUN_0040ee70();
};
FUN_0040ee70::~FUN_0040ee70() {
    second.FUN_0066b0d0(0);
    first.FUN_0066b0d0(0);
}