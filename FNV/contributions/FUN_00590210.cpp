struct FUN_00483370 {
    virtual ~FUN_00483370();
    unsigned int formType;
    unsigned int formFlags;
    unsigned int formId;
    unsigned int formVersion;
    unsigned int formData;
    FUN_00483370();
    void FUN_00483710();
    void FUN_004f15a0(int count);
};
struct FUN_00402c20 {
    virtual ~FUN_00402c20();
    FUN_00402c20();
};
struct FUN_00590210 : FUN_00483370, FUN_00402c20 {
    FUN_00590210();
    virtual ~FUN_00590210();
};
FUN_00590210::FUN_00590210() {
    FUN_00483710();
    FUN_004f15a0(5);
}