struct T
{
    virtual void slot00() = 0;
    virtual void slot01() = 0;
    virtual void slot02() = 0;
    virtual void slot03() = 0;
    virtual void slot04() = 0;
    virtual void slot05() = 0;
    virtual void slot06() = 0;
    virtual void slot07() = 0;
    virtual void slot08() = 0;
    virtual void slot09() = 0;
    virtual void slot10() = 0;
    virtual void slot11() = 0;
    virtual void slot12() = 0;
    virtual void slot13() = 0;
    virtual void slot14() = 0;
    virtual void slot15() = 0;
    virtual void slot16() = 0;
    virtual void slot17() = 0;
    virtual void slot18() = 0;
    virtual void slot19() = 0;
    virtual void slot20() = 0;
    virtual void slot21() = 0;
    virtual void slot22() = 0;
    virtual void slot23() = 0;
    virtual void slot24() = 0;
    virtual void slot25() = 0;
    virtual void slot26() = 0;
    virtual void slot27() = 0;
    virtual void slot28() = 0;
    virtual void slot29() = 0;
    virtual void slot30() = 0;
    virtual void slot31() = 0;
    virtual void slot32() = 0;
    virtual void slot33() = 0;
    virtual void slot34() = 0;
    virtual void slot35() = 0;
    virtual void slot36() = 0;
    virtual void slot37() = 0;
    virtual void slot38() = 0;
    virtual void slot39() = 0;
    virtual void slot40() = 0;
    virtual void slot41() = 0;
    virtual void slot42() = 0;
    virtual void slot43() = 0;
    virtual void slot44() = 0;
    virtual void* Query(char*) = 0;
    void FUN_00cb0120(void*);
    void FUN_00ca4f80(void*);
};

#include <stdlib.h>

void T::FUN_00cb0120(void* arg)
{
    char local;
    volatile unsigned int* data = (volatile unsigned int*)Query(&local);
    unsigned char* context = (unsigned char*)arg;
    if (context[0x1e4] != 1)
    {
        data[0x4] = _byteswap_ulong(data[0x4]);
        data[0x5] = _byteswap_ulong(data[0x5]);
        data[0x6] = _byteswap_ulong(data[0x6]);
        data[0x7] = _byteswap_ulong(data[0x7]);
        data[0x8] = _byteswap_ulong(data[0x8]);
        data[0x9] = _byteswap_ulong(data[0x9]);
        data[0xa] = _byteswap_ulong(data[0xa]);
        data[0xb] = _byteswap_ulong(data[0xb]);
        data[0x10] = 0;
    }
    FUN_00ca4f80(arg);
    if (context[0x1e4] != 1)
    {
        data[0x4] = _byteswap_ulong(data[0x4]);
        data[0x5] = _byteswap_ulong(data[0x5]);
        data[0x6] = _byteswap_ulong(data[0x6]);
        data[0x7] = _byteswap_ulong(data[0x7]);
        data[0x8] = _byteswap_ulong(data[0x8]);
        data[0x9] = _byteswap_ulong(data[0x9]);
        data[0xa] = _byteswap_ulong(data[0xa]);
        data[0xb] = _byteswap_ulong(data[0xb]);
        data[0x10] = 0;
    }
}
