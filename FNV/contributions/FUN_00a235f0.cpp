struct FUN_00a235f0_Row
{
    unsigned int m_value00;
    unsigned int m_value01;
    unsigned int m_value02;
    unsigned int m_value03;
    unsigned int m_value04;
    unsigned int m_value05;
    unsigned int m_value06;
    unsigned int m_value07;
    unsigned int m_value08;
    unsigned int m_value09;
    unsigned int m_value10;
    unsigned int m_value11;
    unsigned int m_value12;
    unsigned int m_value13;
    unsigned int m_value14;
    unsigned int m_value15;
    unsigned int m_value16;
    unsigned int m_value17;
    unsigned int m_value18;
    unsigned int m_value19;
    unsigned int m_value20;
    unsigned int m_value21;
    unsigned int m_value22;
    unsigned int m_value23;
    unsigned int m_value24;
    unsigned int m_value25;
    unsigned int m_value26;
    unsigned int m_value27;
    unsigned int m_value28;
    unsigned int m_value29;
    unsigned int m_value30;
    unsigned int m_value31;
    unsigned int m_field80;
    unsigned int m_field84;
    unsigned int m_field88;
    unsigned int m_field8c;
    unsigned int m_field90;
    unsigned int m_field94;
    unsigned int m_field98;
    unsigned int m_field9c;
};

struct FUN_00a235f0_Class
{
    unsigned int m_field00;
    unsigned int m_field04;
    unsigned int m_field08;
    unsigned int m_field0c;
    unsigned int m_field10;
    unsigned int m_field14;
    unsigned int m_field18;
    unsigned int m_field1c;
    unsigned int m_field20;
    unsigned int m_field24;
    unsigned int m_field28;
    unsigned int m_field2c;
    unsigned int m_field30;
    FUN_00a235f0_Row m_row;

    int __thiscall FUN_00a235f0(int param_1, int param_2);
};

int __thiscall FUN_00a235f0_Class::FUN_00a235f0(int param_1, int param_2)
{
    unsigned int* row = reinterpret_cast<unsigned int*>(
        reinterpret_cast<char*>(this) + param_1 * 0xa0 + 0x34);
    int value = static_cast<int>(row[param_2 + 8]);

    if (static_cast<unsigned short>(value & 0xffff) == 0xffff)
        return -1;

    return value / 0x1194 + 0x20;
}