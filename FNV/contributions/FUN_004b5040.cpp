class FUN_004b50c0 {
public:
    FUN_004b50c0();
    virtual ~FUN_004b50c0();
    void FUN_00c87260(unsigned int value);
};

class FUN_004b5040 : public FUN_004b50c0 {
public:
    FUN_004b5040(unsigned int value);
    virtual ~FUN_004b5040();
};

extern int DAT_01268124;

FUN_004b5040::FUN_004b5040(unsigned int value)
{
    FUN_00c87260(value);
    ++DAT_01268124;
}
