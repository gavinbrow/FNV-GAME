struct Point3 {
    float x;
    float y;
    float z;
    void FUN_00439ef0();
    float FUN_004a7290();
};
template<int N> struct VirtualTag {};
template<int N, class T> struct VirtualLevel : VirtualLevel<N-1, T> {
    virtual void v(VirtualTag<N>*) = 0;
};
template<class T> struct VirtualLevel<0, T> {
    virtual void v(VirtualTag<0>*) = 0;
};
struct InputActor;
struct OutputActor;
template<> struct VirtualLevel<125, InputActor> : VirtualLevel<124, InputActor> {
    virtual Point3* GetPosition() = 0;
};
template<> struct VirtualLevel<125, OutputActor> : VirtualLevel<124, OutputActor> {
    virtual Point3* ComputePosition(Point3*, Point3*) = 0;
};
struct InputActor : VirtualLevel<125, InputActor> {};
struct OutputActor : VirtualLevel<265, OutputActor> {
    virtual IMH* GetIMH() = 0;
};
struct RelevantTarget { void* handle; InputActor* originalActor; };
struct CombatStateView { RelevantTarget* FUN_007058c0(); };
extern double DAT_0108d6e8;

struct SearchGroup : CombatGroup_GetCount {
    OutputActor* FUN_0098cd50(InputActor* source, OutputActor* priority, float radius);
};

OutputActor* SearchGroup::FUN_0098cd50(InputActor* source, OutputActor* priority, float radius)
{
    float bestDistance = radius * radius;
    OutputActor* bestActor = 0;
    Point3 center2 = *source->GetPosition();
    unsigned int numberOfActors3 = GetCount();
    for (unsigned int index = 0; index < numberOfActors3; ++index) {
        OutputActor* actor4 = reinterpret_cast<OutputActor*>(reinterpret_cast<FUN_00986b70_helper*>(this)->FUN_00903600(index));
        if (actor4 == reinterpret_cast<OutputActor*>(source))
            continue;
        Point3 delta;
        actor4->ComputePosition(&delta, &center2)->FUN_00439ef0();
        float squaredDistance = delta.FUN_004a7290();
        if (actor4 == priority)
            squaredDistance = (float)(squaredDistance / DAT_0108d6e8);
        if (squaredDistance < bestDistance) {
            bestDistance = squaredDistance;
            bestActor = actor4;
        }
    }
    if (bestActor) {
        IMH* handle = bestActor->GetIMH();
        if (handle) {
            RelevantTarget* target = reinterpret_cast<CombatStateView*>(handle->FUN_00586150())->FUN_007058c0();
            if (target && target->originalActor == source)
                bestActor = 0;
        }
    }
    return bestActor;
}
