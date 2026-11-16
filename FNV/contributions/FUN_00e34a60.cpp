struct AnimDispatch {
    virtual void Slot00();
    virtual void Slot04();
    virtual void Slot08();
    virtual void Slot0c();
    virtual void Dispatch(float frameTime, int sectionA, int sourceA, int sectionB, int sourceB, int count);
    int m_04;
    int m_08;
    int m_0c;
    int m_sectionA;
    int m_sectionB;
    void FUN_00e34a60(float frameTime, int sourceA, int sourceB, int count);
};
void AnimDispatch::FUN_00e34a60(float frameTime, int sourceA, int sourceB, int count)
{
    Dispatch(frameTime, m_sectionA, sourceA, m_sectionB, sourceB, count);
}