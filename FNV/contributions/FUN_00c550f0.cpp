extern "C" void* g_012031e8;
extern unsigned int DAT_010c1040;
extern unsigned int DAT_010c2bf8;

struct W5Sub {
    int pad;
    unsigned int __thiscall FUN_00a59af0(void* desc);
};

struct W5Big {
    int u00;
    int u04;
    int u08;
    int u0c;
    int u10;
    int u14;
    int u18;
    int u1c;
    int u20;
    void* p;
};

struct W5Self {
    int f00;
    int f04;
    int f08;
    W5Sub subC;
    int f10;
    int f14;
    W5Sub sub18;
    void __thiscall FUN_00a7b580(ArrC43220* a1);
    void __thiscall FUN_00c550f0(ArrC43220* a1);
};

void W5Self::FUN_00c550f0(ArrC43220* a1) {
    FUN_00a7b580(a1);
    unsigned int r1;
    unsigned int p;
    unsigned int r2;
    {
        W5Big big;
        big.p = g_012031e8;
        p = (unsigned int)FUN_00a7d330(big.p);
        a1->FUN_0096a610(p);
        r1 = subC.FUN_00a59af0(&DAT_010c1040);
        a1->FUN_0096a610(r1);
        r2 = sub18.FUN_00a59af0(&DAT_010c2bf8);
        a1->FUN_0096a610(r2);
    }
}
