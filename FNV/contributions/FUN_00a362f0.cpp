extern const float DAT_01015f5c;
extern "C" int DAT_011a8400;
extern "C" int DAT_011a8404;
extern "C" int DAT_011a8408;
extern "C" int DAT_011f3704;
extern "C" int DAT_011f3708;
extern "C" int DAT_011f370c;
extern "C" int DAT_011f3710;
extern "C" float DAT_01096b8c;

struct Card9 {
    int a0; int a1; int a2; int a3; int a4; int a5; int a6; int a7; int a8;
};
extern "C" Card9 DAT_011a9448;

union Fld { int i; float f; };

class FUN_00a362f0_cls {
public:
    float m_f00;
    Fld m_f04;
    Fld m_f08;
    Fld m_f0c;
    Fld m_f10;
    Fld m_f14;
    Fld m_f18;
    Fld m_f1c;
    Fld m_f20;
    Fld m_f24;
    Fld m_f28;
    Fld m_f2c;
    Fld m_f30;
    Fld m_f34;
    Fld m_f38;
    Fld m_f3c;
    Fld m_f40;
    Card9 m_arr;
    void* FUN_00a362f0();
};

void* FUN_00a362f0_cls::FUN_00a362f0()
{
    volatile float* __restrict p = (volatile float*)this;

    m_f04.i = DAT_011a8400;
    m_f08.i = DAT_011a8404;
    m_f0c.i = DAT_011a8408;
    m_f10.i = DAT_011f3704;
    m_f14.i = DAT_011f3708;
    m_f18.i = DAT_011f370c;
    m_f1c.i = DAT_011f3710;
    m_f20.f = DAT_01096b8c;
    m_f24.i = DAT_011a8400;
    m_f28.i = DAT_011a8404;
    m_f2c.i = DAT_011a8408;
    m_f30.i = DAT_011f3704;
    m_f34.i = DAT_011f3708;
    m_f38.i = DAT_011f370c;
    m_f3c.i = DAT_011f3710;
    m_f40.f = DAT_01096b8c;

    p[0] = DAT_01015f5c;
    p[1] = DAT_01015f5c;
    p[5] = DAT_01015f5c;
    p[8] = DAT_01015f5c;
    p[9] = DAT_01015f5c;
    p[13] = DAT_01015f5c;
    m_f40.f = DAT_01015f5c;

    m_arr = DAT_011a9448;
    return this;
}