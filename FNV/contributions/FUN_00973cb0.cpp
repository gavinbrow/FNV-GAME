struct FUN_00973cb0_cls : public ProcessLists { void FUN_00973cb0(Actor* target); };
void FUN_00973cb0_cls::FUN_00973cb0(Actor* target) {
    MobileObject* object = 0;
    for (unsigned int i = 0; i < MobProcessArray.GetTail((PROCESS_TYPE)0); ++i) {
        object = MobProcessArray.GetItem(i);
        Actor* actor = 0;
        if (object) {
            if (object->IsActor())
                actor = (Actor*)object;
        }
        if (actor) {
            actor->GetCurrentAIProcess()->RemoveDetectionActor(target, (BaseProcess::DetectionListType)3);
        }
    }
}