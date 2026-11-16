#include "h_d1fadad83c84.h"

struct ActorMover_008b3840
{
    void SetMoveMode(unsigned int moveMode);
};

struct FUN_008b3840_Actor : public Actor
{
    void FUN_008b3840(unsigned int moveMode);
};

void FUN_008b3840_Actor::FUN_008b3840(unsigned int moveMode)
{
    reinterpret_cast<ActorMover_008b3840*>(pActorMover)->SetMoveMode(moveMode);
}