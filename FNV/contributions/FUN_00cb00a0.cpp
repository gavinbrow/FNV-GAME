struct StreamData
{
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int value10;
    unsigned int value14;
    unsigned int value18;
    unsigned int value1C;
    unsigned int value20;
    unsigned int value24;
    unsigned int value28;
    unsigned int value2C;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3C;
    unsigned int flags40;
};

struct FUN_00cb00a0_Class
{
    void FUN_00ca4ec0(char*);
    virtual void* slot00(void*);
    virtual void* slot01(void*);
    virtual void* slot02(void*);
    virtual void* slot03(void*);
    virtual void* slot04(void*);
    virtual void* slot05(void*);
    virtual void* slot06(void*);
    virtual void* slot07(void*);
    virtual void* slot08(void*);
    virtual void* slot09(void*);
    virtual void* slot10(void*);
    virtual void* slot11(void*);
    virtual void* slot12(void*);
    virtual void* slot13(void*);
    virtual void* slot14(void*);
    virtual void* slot15(void*);
    virtual void* slot16(void*);
    virtual void* slot17(void*);
    virtual void* slot18(void*);
    virtual void* slot19(void*);
    virtual void* slot20(void*);
    virtual void* slot21(void*);
    virtual void* slot22(void*);
    virtual void* slot23(void*);
    virtual void* slot24(void*);
    virtual void* slot25(void*);
    virtual void* slot26(void*);
    virtual void* slot27(void*);
    virtual void* slot28(void*);
    virtual void* slot29(void*);
    virtual void* slot30(void*);
    virtual void* slot31(void*);
    virtual void* slot32(void*);
    virtual void* slot33(void*);
    virtual void* slot34(void*);
    virtual void* slot35(void*);
    virtual void* slot36(void*);
    virtual void* slot37(void*);
    virtual void* slot38(void*);
    virtual void* slot39(void*);
    virtual void* slot40(void*);
    virtual void* slot41(void*);
    virtual void* slot42(void*);
    virtual void* slot43(void*);
    virtual void* slot44(void*);
    virtual StreamData* getData(void*);
    void FUN_00cb00a0(char*);
};

#include <stdlib.h>

void FUN_00cb00a0_Class::FUN_00cb00a0(char* object)
{
    this->FUN_00ca4ec0(object);
    if (object[0x1e5] != 1)
    {
        void* out;
        volatile StreamData* data = (volatile StreamData*)this->getData(&out);
        data->value10 = _byteswap_ulong(data->value10);
        data->value14 = _byteswap_ulong(data->value14);
        data->value18 = _byteswap_ulong(data->value18);
        data->value1C = _byteswap_ulong(data->value1C);
        data->value20 = _byteswap_ulong(data->value20);
        data->value24 = _byteswap_ulong(data->value24);
        data->value28 = _byteswap_ulong(data->value28);
        data->value2C = _byteswap_ulong(data->value2C);
        data->flags40 = 0;
    }
}






