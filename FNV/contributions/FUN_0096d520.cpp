
struct CellProcessState {
    BSSimpleList<MobileObject*>* currentActors;
    int generation;
    int count;
    BSSimpleList<MobileObject*>* actors;
};

struct CellProcessType {
    int FUN_0041ca90();
};

struct CellProcessManager {
    CellProcessState* FUN_00422700();
    void FUN_00422690(MobileObject* actor);
    void FUN_00422720();
    CellProcessType* FUN_0041cb10();
};

struct ActorProcessProxy {
    CellProcessManager* FUN_005d43c0();
    int FUN_008d8520();
    CellProcessType* FUN_00881510();
    int FUN_00931850();
    void FUN_00881680(int flag);
};

extern float DAT_01084838;


void __cdecl FUN_0096d520()
{
    CellProcessState* current =
        reinterpret_cast<ActorProcessProxy*>(pPlayer)->FUN_005d43c0()->FUN_00422700();
    if (current) {
        BSSimpleList<MobileObject*>* removedActors;
        BSSimpleList<MobileObject*>* nextIt;
        BSSimpleList<MobileObject*>* actorsToExamine;
        actorsToExamine = new BSSimpleList<MobileObject*>();
        nextIt = new BSSimpleList<MobileObject*>();

        BSSimpleList<MobileObject*>* firstIt = nextIt;
        removedActors = current->actors;
        while (removedActors && removedActors->GetItem()) {
            nextIt->AddTail(removedActors->GetItem());
            removedActors = removedActors->GetNext();
        }

        while (firstIt && firstIt->GetItem()) {
            MobileObject* actor = firstIt->GetItem();
            if (actor && actor != pPlayer) {
                if (reinterpret_cast<ActorProcessProxy*>(actor)->FUN_008d8520()) {
                    CellProcessType* process = reinterpret_cast<ActorProcessProxy*>(actor)->FUN_00881510();
                    CellProcessType* replacement = reinterpret_cast<ActorProcessProxy*>(actor)->FUN_005d43c0()->FUN_0041cb10();
                    if (replacement)
                        process = replacement;
                    if (!process ||
                        (process->FUN_0041ca90() != 1 && process->FUN_0041ca90() != 7)) {
                        actorsToExamine->AddHead(actor);
                    } else {
                        int result = reinterpret_cast<ActorProcessProxy*>(actor)->FUN_00931850();
                        if (result) {
                            typedef void (__thiscall *VirtualAction)(MobileObject*, int);
                            typedef void (__thiscall *VirtualFloat)(MobileObject*, float);
                            reinterpret_cast<VirtualAction>((*reinterpret_cast<void***>(actor))[0x10D])(actor, 0);
                            reinterpret_cast<ActorProcessProxy*>(actor)->FUN_00881680(0);
                            reinterpret_cast<VirtualFloat>((*reinterpret_cast<void***>(actor))[0x97])(actor, DAT_01084838);
                        }
                    }
                }
            }
            firstIt = firstIt->GetNext();
        }

        firstIt = actorsToExamine;
        while (firstIt && firstIt->GetItem()) {
            MobileObject* actorToRemove = firstIt->GetItem();
            reinterpret_cast<ActorProcessProxy*>(pPlayer)->FUN_005d43c0()->FUN_00422690(actorToRemove);
            firstIt = firstIt->GetNext();
        }

        actorsToExamine->RemoveAll();
        delete actorsToExamine;
        nextIt->RemoveAll();
        delete nextIt;
        if (current->actors->IsEmpty())
            reinterpret_cast<ActorProcessProxy*>(pPlayer)->FUN_005d43c0()->FUN_00422720();
    }
}
