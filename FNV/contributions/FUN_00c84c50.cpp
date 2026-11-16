struct FUN_00c877b0 {
    virtual ~FUN_00c877b0();
};

struct FUN_00c84c50 : FUN_00c877b0 {
    virtual ~FUN_00c84c50();
};

void FUN_00c876a0();
extern int DAT_012680f8;

FUN_00c84c50::~FUN_00c84c50() {
    FUN_00c876a0();
    --DAT_012680f8;
}
