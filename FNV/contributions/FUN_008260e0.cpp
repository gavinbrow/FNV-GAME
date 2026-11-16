#include <new>
struct FUN_008260b0 {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
    virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
    virtual void v16(); virtual void Install(FUN_008260b0*);
    float value04;
    void* object08;
    void* object0c;
    bool flag10, flag11, flag12, flag13;
    int unk14, unk18;
    float value1c, value20;
    int unk24;
    void* object28;
    int unk2c;
    int unk30, unk34, unk38, unk3c, unk40, unk44;
    FUN_008260b0(void*, void*, void*);
    FUN_008260b0* FUN_008260e0();
};
FUN_008260b0* FUN_008260b0::FUN_008260e0() {
    FUN_008260b0* result = new FUN_008260b0(object28, object08, object0c);
    Install(result);
    return result;
}
