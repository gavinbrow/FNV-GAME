struct FUN_0067ad70 {
    virtual ~FUN_0067ad70();
};
struct LocationShell {
    ~LocationShell();
};
struct FUN_0067c7d0 : FUN_0067ad70 {
    LocationShell* pSearchLocation;
    virtual ~FUN_0067c7d0();
};
FUN_0067c7d0::~FUN_0067c7d0() {
    delete pSearchLocation;
}
