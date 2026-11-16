extern unsigned int DAT_010173f0;
extern int DAT_010a307c;

struct FUN_00ec78e0 {
    void* vtbl;
    int unk04;
    int unk08;

    FUN_00ec78e0();
};

struct FUN_00b096a0_Str {
    void FUN_0044a730(bool, unsigned int);
    void FUN_0044a580(const FUN_00b096a0_Str&, unsigned int, unsigned int);

    ~FUN_00b096a0_Str();
};

struct FUN_00b096a0 : FUN_00ec78e0 {
    FUN_00b096a0_Str m_str;

    FUN_00b096a0(const FUN_00b096a0_Str& pName);
};

FUN_00b096a0::FUN_00b096a0(const FUN_00b096a0_Str& pName)
{
    int v00;
    int v01;
    int v02;
    int v03;
    int v04;
    int v05;
    int v06;
    int v07;
    int v08;
    int v09;
    int v10;
    int v11;
    int v12;
    int v13;
    int v14;
    int v15;
    int v16;
    int v17;
    int v18;
    int v19;
    int v20;
    int v21;
    int v22;
    int v23;
    int v24;
    int v25;

    *(void**)this = (void*)&DAT_010a307c;

    {
        FUN_00b096a0_Str& s = m_str;
        s.FUN_0044a730(false, 0);
        s.FUN_0044a580(pName, 0, DAT_010173f0);
    }
}
