struct FUN_0098f580_Item
{
    int m_00;
    int m_04;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    int m_1c;
    int m_20;
    int m_24;
    int m_28;
    int m_2c;
    int m_30;
    int m_34;
    int m_38;
    int m_3c;
    int m_40;
    int m_44;
    int m_48;
    int m_4c;
    int m_50;
    int m_54;
    int m_58;
    int m_5c;
    int m_60;
    int m_64;
};

struct FUN_0096a330_class
{
    void __thiscall FUN_0098ed80(unsigned int, int);
    FUN_0098f580_Item* __thiscall FUN_0096a330(int);
};

struct FUN_0098f580_class
{
    void* m_00;
    FUN_0098f580_Item* m_items;
    unsigned int m_count;

    void __thiscall FUN_0098f580(FUN_0096a330_class* destination);
};

void __thiscall FUN_0098f580_class::FUN_0098f580(
    FUN_0096a330_class* destination)
{
    destination->FUN_0098ed80(m_count, 1);

    for (unsigned int index = 0; index < m_count; ++index)
        *destination->FUN_0096a330(index) = m_items[index];
}