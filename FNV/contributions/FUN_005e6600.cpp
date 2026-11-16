// FUN_005e6600: real destructor (__thiscall, no params) of a class with:
//   - a polymorphic base at offset 0 (total size 8, its dtor at 0x5e6470)
//   - a member object at offset 8 whose dtor is 0x5aa1a0
//   - a destructor body calling this->FUN_005e6c60(0)

struct FUN_005e6470 {
    virtual ~FUN_005e6470();
    void FUN_005e6c60(int);
    int unk04;
};

struct FUN_005aa1a0 {
    ~FUN_005aa1a0();
};

struct FUN_005e6600 : FUN_005e6470 {
    FUN_005aa1a0 unk08;
    ~FUN_005e6600();
};

FUN_005e6600::~FUN_005e6600()
{
    this->FUN_005e6c60(0);
}
