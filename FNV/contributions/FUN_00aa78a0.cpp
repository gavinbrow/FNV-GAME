extern "C" unsigned int DAT_010a28fc;
struct FUN_00aa8ca0_cls
{
    void* m_vtable;
    unsigned char m_data[0x20ec];
    FUN_00aa8ca0_cls(int a, int b, int c, int size) { FUN_00aa8ca0(a,b,c,size); }
    ~FUN_00aa8ca0_cls();
    FUN_00aa8ca0_cls* FUN_00aa8ca0(int a,int b,int c,int size);
};
struct FUN_00aa78a0_cls : FUN_00aa8ca0_cls {
    unsigned char m_option;
    unsigned char m_ready;
    FUN_00aa78a0_cls(int a,int b,int c,unsigned char option);
    void FUN_00aa8dd0();
};
// @fnv 0x00aa78a0
FUN_00aa78a0_cls::FUN_00aa78a0_cls(int a,int b,int c,unsigned char option):FUN_00aa8ca0_cls(a,b,c,0x10000)
{m_vtable=&DAT_010a28fc;m_option=option;m_ready=0;FUN_00aa8dd0();}
