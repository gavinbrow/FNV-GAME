extern char DAT_010ce81c;
struct AgentDispatchDescriptor {
    const void* dispatchTable;
    unsigned char isFlipped;
    volatile unsigned int tag;
};
struct CollisionDispatcher {
    void FUN_00d3e510(void* bodyB, void* bodyA, void* input, AgentDispatchDescriptor* descriptor);
    void FUN_00d3f000(void* bodyA, void* bodyB, void* volatile input, unsigned int tag);
};
void CollisionDispatcher::FUN_00d3f000(void* bodyA, void* bodyB, void* volatile input, unsigned int tag)
{
    AgentDispatchDescriptor descriptor;
    descriptor.tag = tag;
    descriptor.isFlipped = false;
    descriptor.dispatchTable = &DAT_010ce81c;
    FUN_00d3e510(bodyB, bodyA, input, &descriptor);
}