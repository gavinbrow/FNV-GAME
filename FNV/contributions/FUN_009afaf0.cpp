struct VectorHolder {
    unsigned int handle;
    void __thiscall FUN_006815c0();
    void __thiscall FUN_00537e90(unsigned int);
    VectorHolder() { FUN_006815c0(); }
};
struct BaseObject {
    virtual ~BaseObject();
    unsigned int unk04;
    void __thiscall FUN_00621060();
    BaseObject() { FUN_00621060(); }
};
struct FUN_009afaf0 : BaseObject {
    VectorHolder first;
    VectorHolder second;
    VectorHolder third;
    VectorHolder fourth;
    FUN_009afaf0(unsigned int firstValue, unsigned int secondValue);
    virtual ~FUN_009afaf0();
};
FUN_009afaf0::FUN_009afaf0(unsigned int firstValue, unsigned int secondValue) {
    first.FUN_00537e90(firstValue);
    second.FUN_00537e90(firstValue);
    third.FUN_00537e90(secondValue);
    fourth.FUN_00537e90(0);
}