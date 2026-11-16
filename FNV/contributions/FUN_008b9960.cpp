void __cdecl FUN_008b9960(ActorValueOwner* owner, ActorValue::Index av, float previousValue, float change)
{
    if (!owner || (av != (ActorValue::Index)16 && av != (ActorValue::Index)22))
        return;
    float newValue;
    Actor* actor = static_cast<Actor*>(owner);
    if (!actor->pCurrentProcess)
        return;
    newValue = previousValue + change;
    float permanentValue = owner->GetPermanentActorFloatValue(av);
    {
        bool decrease = change < _gModifierZero && newValue < permanentValue;
        bool increase = change > _gModifierZero && newValue >= permanentValue;
        if (decrease) {
            if (av == (ActorValue::Index)16)
                ((FUN_008acf70_s*)actor->pCurrentProcess)->FUN_008acf70(0x20000000, true);
            else if (av == (ActorValue::Index)22)
                ((FUN_008acf70_s*)actor->pCurrentProcess)->FUN_008acf70(0x40000000, true);
        } else if (increase) {
            if (av == (ActorValue::Index)16)
                ((FUN_008acf70_s*)actor->pCurrentProcess)->FUN_008acf70(0x20000000, false);
            else if (av == (ActorValue::Index)22)
                ((FUN_008acf70_s*)actor->pCurrentProcess)->FUN_008acf70(0x40000000, false);
        }
    }
}