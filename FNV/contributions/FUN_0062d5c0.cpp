extern "C" int DAT_0104e37c;
extern "C" int DAT_0104e350;
extern "C" int DAT_0104e338;

struct FUN_0061ffb0 {
    int* m_vtable;
    int m_data04;
    FUN_0061ffb0();
    ~FUN_0061ffb0();
};

struct FUN_0062d680 {
    int* m_vtable;
    int m_data04;
    int m_data08;
    int m_data0c;
    int m_data10;
    FUN_0062d680();
};

struct FUN_0062d5c0 : FUN_0061ffb0 {
    FUN_0062d680 m_part08;
    int* m_vtable1c;
    int m_count20;
    FUN_0062d5c0();
};

FUN_0062d5c0::FUN_0062d5c0()
    : FUN_0061ffb0(), m_part08() {
    m_vtable = &DAT_0104e37c;
    m_part08.m_vtable = &DAT_0104e350;
    m_vtable1c = &DAT_0104e338;
    m_count20 = 0;
}
