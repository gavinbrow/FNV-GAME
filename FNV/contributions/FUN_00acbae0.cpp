struct FUN_00acbae0_Value {
    unsigned int m_00;
    unsigned int m_04;
    unsigned __int64 m_08;
    unsigned int m_10;
};
class FUN_00acbae0_cls {
public:
    FUN_00acbae0_Value* __thiscall FUN_00acbae0(FUN_00acbae0_Value* out, unsigned int a2, unsigned int a3, unsigned int a4);
};
FUN_00acbae0_Value* FUN_00acbae0_cls::FUN_00acbae0(FUN_00acbae0_Value* out, unsigned int a2, unsigned int a3, unsigned int a4) {
    unsigned int value = DAT_010f1e40;
    out->m_00 = value;
    out->m_08 = 0;
    out->m_10 = DAT_01011d78;
    return out;
}