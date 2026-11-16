struct FUN_0058bc00_obj {
    void __fastcall FUN_0058bc00();
};

void __fastcall FUN_0058b830(FUN_0058bc00_obj* this_ptr);

struct FUN_0058b450 {
    ~FUN_0058b450();
};

struct FUN_0058b7d0 : FUN_0058b450 {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    FUN_0058bc00_obj m_18;

    ~FUN_0058b7d0();
};

FUN_0058b7d0::~FUN_0058b7d0() {
    FUN_0058b830(&m_18);
}
