struct FUN_00538ef0 {
    virtual void VirtualMethod();
    ~FUN_00538ef0();
    int m_a;
    int m_b;
    FUN_00538ef0();
};

struct FUN_0056d640 : FUN_00538ef0 {
    B006815c0 m_quantity;
    FUN_0056d640(unsigned int quantity);
};

FUN_0056d640::FUN_0056d640(unsigned int quantity)
    : FUN_00538ef0(), m_quantity()
{
    m_b = 0;
    reinterpret_cast<FUN_00537e90*>(&m_quantity)->SetQuantity(quantity);
}
