extern float DAT_0104da48;
struct hkpSymmetricAgentFlipCollector
{
    virtual void dispose();
    virtual void collect(float value);
    virtual void process(void* value);
    float threshold;
    void* object;
};
struct Context
{
    void FUN_00d43880(void* first, void* second, void* third, hkpSymmetricAgentFlipCollector* collector);
    void FUN_00d2edd0(void* first, void* second, void* third, void* fourth);
};
void Context::FUN_00d2edd0(void* first, void* second, void* third, void* fourth)
{
    hkpSymmetricAgentFlipCollector collector;
    collector.threshold = DAT_0104da48;
    collector.object = fourth;
    FUN_00d43880(second, first, third, &collector);
}
