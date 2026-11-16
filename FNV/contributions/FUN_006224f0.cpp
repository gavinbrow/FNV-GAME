struct CellMoppBaseView_006815c0 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int m10;
    int m14;
    float m18;
    float m1c;
    void FUN_006815c0();
    void FUN_004b4d50(float a, float b, float c, float d);
};
struct CellMoppMemberView_00622570 {
    unsigned char m_b;
    void FUN_006815c0();
    unsigned char* FUN_00622570(unsigned char b);
};
extern float DAT_01012054;
struct CellMoppCtor_006224f0 : CellMoppBaseView_006815c0 {
    CellMoppMemberView_00622570 m20;
    CellMoppCtor_006224f0* FUN_006224f0();
};
CellMoppCtor_006224f0* CellMoppCtor_006224f0::FUN_006224f0()
{
    ((CellMoppBaseView_006815c0*)this)->FUN_006815c0();
    m20.FUN_006815c0();
    FUN_004b4d50(1.0f, 1.0f, 1.0f, 0.0f);
    m10 = 2;
    m14 = 2;
    m18 = 0.0f;
    m1c = DAT_01012054;
    m20.FUN_00622570(0);
    return this;
}