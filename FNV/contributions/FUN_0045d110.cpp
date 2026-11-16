struct FUN_0045d110;

struct FUN_0045d180_Interface {
    virtual ~FUN_0045d180_Interface();
    virtual void unk04();
    virtual void unk08(FUN_0045d110*);
};

FUN_0045d180_Interface* __cdecl FUN_0045d180();

struct FUN_0045d110 : FUN_00404950 {
    virtual ~FUN_0045d110();
};

FUN_0045d110::~FUN_0045d110() {
    FUN_0045d180()->unk08(this);
}
