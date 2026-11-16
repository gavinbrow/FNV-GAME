template <int N> struct VirtualSlotTag {};
template <int N> struct OpaqueVirtualInterface : OpaqueVirtualInterface<N-1> {
    virtual void UnresolvedVirtual(VirtualSlotTag<N>*);
};
template <> struct OpaqueVirtualInterface<0> {
    virtual void UnresolvedVirtual(VirtualSlotTag<0>*);
};
struct DispatchActor : OpaqueVirtualInterface<351> {
    virtual void Refresh(int, int, int);
};
struct ActorBridge {
    DispatchActor* FUN_008d8520();
};
struct ActiveEffectListBridge {
    bool FUN_008256d0();
    ActiveEffect** FUN_006815c0();
    ActiveEffectListBridge* FUN_00726070();
};
void __cdecl FUN_00806130(ActiveEffectListBridge* list, ActorBridge* actor)
{
    while (list != 0 && !list->FUN_008256d0()) {
        ActiveEffect* effect = *list->FUN_006815c0();
        effect->FinishInitLoadGame(reinterpret_cast<Actor*>(actor));
        list = list->FUN_00726070();
    }
    if (actor != 0) {
        if (actor->FUN_008d8520()) {
            DispatchActor* dispatcher = actor->FUN_008d8520();
            dispatcher->Refresh(1, 1, 1);
        }
    }
}