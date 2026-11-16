class hkpShapeD923 {
public:
    virtual ~hkpShapeD923();
    unsigned short m_memSizeAndFlags;
    short m_referenceCount;
    unsigned int m_userData;
    int m_type;
};
struct hkpCdBodyD923 {
    const hkpShapeD923* m_shape;
    unsigned int m_shapeKey;
    const void* m_motion;
    const hkpCdBodyD923* m_parent;
};
class hkpContactMgrD923;
class hkpCollisionAgentD923;
struct hkpCollisionInputD923;
typedef hkpCollisionAgentD923* (__cdecl *CreateFuncD923)(
    const hkpCdBodyD923&, const hkpCdBodyD923&,
    const hkpCollisionInputD923&, hkpContactMgrD923*);
struct AgentFuncsD923 {
    CreateFuncD923 m_createFunc;
    void* m_getPenetrationsFunc;
    void* m_getClosestPointFunc;
    void* m_linearCastFunc;
    void* m_isFlipped;
};
struct hkpCollisionDispatcherD923 {
    int unk000;
    int unk004;
    int unk008;
    int unk00c;
    int unk010;
    int unk014;
    int unk018;
    int unk01c;
    int unk020;
    int unk024;
    int unk028;
    int unk02c;
    int unk030;
    int unk034;
    int unk038;
    int unk03c;
    int unk040;
    int unk044;
    int unk048;
    int unk04c;
    int unk050;
    int unk054;
    int unk058;
    int unk05c;
    int unk060;
    int unk064;
    int unk068;
    int unk06c;
    int unk070;
    int unk074;
    int unk078;
    int unk07c;
    int unk080;
    int unk084;
    int unk088;
    int unk08c;
    int unk090;
    int unk094;
    int unk098;
    int unk09c;
    int unk0a0;
    int unk0a4;
    int unk0a8;
    int unk0ac;
    int unk0b0;
    int unk0b4;
    int unk0b8;
    int unk0bc;
    int unk0c0;
    int unk0c4;
    int unk0c8;
    int unk0cc;
    int unk0d0;
    int unk0d4;
    int unk0d8;
    int unk0dc;
    int unk0e0;
    int unk0e4;
    int unk0e8;
    int unk0ec;
    int unk0f0;
    int unk0f4;
    int unk0f8;
    int unk0fc;
    int unk100;
    int unk104;
    int unk108;
    int unk10c;
    int unk110;
    int unk114;
    int unk118;
    int unk11c;
    int unk120;
    int unk124;
    int unk128;
    int unk12c;
    int unk130;
    int unk134;
    int unk138;
    int unk13c;
    int unk140;
    int unk144;
    int unk148;
    int unk14c;
    int unk150;
    int unk154;
    int unk158;
    int unk15c;
    int unk160;
    int unk164;
    int unk168;
    int unk16c;
    int unk170;
    int unk174;
    int unk178;
    int unk17c;
    int unk180;
    int unk184;
    int unk188;
    int unk18c;
    int unk190;
    int unk194;
    int unk198;
    int unk19c;
    unsigned char m_agent2Types[32][32];
    unsigned char m_agent2TypesPred[32][32];
    AgentFuncsD923 m_agent2Func[1];
    CreateFuncD923 findCreateFunc(const hkpCdBodyD923& bodyA, const hkpCdBodyD923& bodyB, const hkpCollisionInputD923& input) const;
};
struct hkpCollisionInputD923 {
    hkpCollisionDispatcherD923* m_dispatcher;
    int unk04, unk08, unk0C, unk10;
    int m_createPredictiveAgents;
};
struct hkpAgent3InputD923 {
    const hkpCdBodyD923* m_bodyA;
    const hkpCdBodyD923* m_bodyB;
    const void* m_overrideBodyA;
    const hkpCollisionInputD923* m_input;
    hkpContactMgrD923* m_contactMgr;
};
struct hkpAgentEntryD923 {
    unsigned char m_streamCommand;
    unsigned char m_agentType;
    unsigned char m_numContactPoints;
    unsigned char m_size;
};
struct hkpAgentDataD923;
inline CreateFuncD923 hkpCollisionDispatcherD923::findCreateFunc(const hkpCdBodyD923& bodyA, const hkpCdBodyD923& bodyB, const hkpCollisionInputD923& input) const
{
    int typeA = bodyA.m_shape->m_type;
    int typeB = bodyB.m_shape->m_type;
    const unsigned char* table = input.m_createPredictiveAgents ? &m_agent2TypesPred[0][0] : &m_agent2Types[0][0];
    unsigned char agentType = table[typeA * 32 + typeB];
    return m_agent2Func[agentType].m_createFunc;
}

hkpAgentDataD923* __cdecl FUN_00d92300(const hkpAgent3InputD923& input,
                                       hkpAgentEntryD923* entry,
                                       hkpAgentDataD923* freeMemory)
{
    entry->m_streamCommand = (entry->m_streamCommand & 8) | 6;
    hkpContactMgrD923* mgr = input.m_contactMgr;
    const hkpCdBodyD923* bodyB = input.m_bodyB;
    const hkpCdBodyD923* bodyA = input.m_bodyA;
    const hkpCollisionInputD923* in = input.m_input;
    hkpCollisionDispatcherD923* disp = in->m_dispatcher;
    CreateFuncD923 f = disp->findCreateFunc(*bodyA, *bodyB, *in);
    hkpCollisionAgentD923* agent = f(*bodyA, *bodyB, *in, mgr);
    *reinterpret_cast<hkpCollisionAgentD923**>(freeMemory) = agent;
    entry->m_numContactPoints = 0xff;
    return reinterpret_cast<hkpAgentDataD923*>(reinterpret_cast<char*>(freeMemory) + 16);
}