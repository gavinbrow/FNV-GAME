#include "h_caaea195bf4f.h"
bool __cdecl FUN_00406d70(int actorValue, unsigned int mask);
bool __cdecl FUN_0066ee10(int actorValue);
void __cdecl FUN_00704e10(int actorValue);
void __cdecl FUN_0066ee50(ActorValueOwner* owner, int actorValue, float previousValue, float currentValue, ActorValueOwner* source);
class PlayerCharacterValueUpdates : public PlayerCharacter {
public:
    int FUN_00880850(int actorValue, int amount, PlayerCharacter* source);
    void FUN_008808f0(int actorValue, int clearFlag);
    void FUN_0094c4f0(int updateType, int actorValue, float value, int operation);
    void FUN_0093ae80(int actorValue, int amount, PlayerCharacter* source);
};
void PlayerCharacterValueUpdates::FUN_0093ae80(int actorValue, int amount, PlayerCharacter* source)
{
    if (FUN_00406d70(actorValue, 0x100))
        return;
    amount = FUN_00880850(actorValue, amount, source);
    float previous = FUN_0066ee10(actorValue)
        ? GetActorFloatValue(static_cast<ActorValue::Index>(actorValue))
        : 0.0f;
    FUN_0094c4f0(0, actorValue, static_cast<float>(amount), 2);
    FUN_00704e10(actorValue);
    if (actorValue == 16 && amount < 0) {
        typedef void (__thiscall *HealthUpdate)(PlayerCharacterValueUpdates*, PlayerCharacter*, float);
        reinterpret_cast<HealthUpdate>((*reinterpret_cast<void***>(this))[0x12e])(
            this, source, static_cast<float>(amount));
    }
    FUN_008808f0(actorValue, 0);
    FUN_0066ee50(static_cast<ActorValueOwner*>(this), actorValue, previous,
                 static_cast<float>(amount), static_cast<ActorValueOwner*>(source));
}