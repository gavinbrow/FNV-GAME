struct Vector3 {
    float x;
    float y;
    float z;
};
extern Vector3 DAT_011f426c;

struct SaveNodeExtended : SaveNodeCls {
    bool FUN_008256d0();
    void FUN_0063f7b0();
    ~SaveNodeExtended();
};

struct DetClassExtended : DetClassCls {
    void FUN_0066e200();
};

void DetClassExtended::FUN_0066e200()
{
    m_00 = 0;
    while (m_04 && !reinterpret_cast<SaveNodeExtended*>(m_04)->FUN_008256d0()) {
        SaveItemCls* item = *m_04->FUN_006815c0();
        FUN_00401030(item);
        reinterpret_cast<SaveNodeExtended*>(m_04)->FUN_0063f7b0();
    }

    delete reinterpret_cast<SaveNodeExtended*>(m_04);
    m_04 = 0;
    *reinterpret_cast<Vector3*>(m_08) = DAT_011f426c;
}
