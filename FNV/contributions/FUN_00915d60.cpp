
extern "C" Actor* DAT_011dea3c;

struct WeaponEquipmentAccess {
    unsigned char FUN_004bda70(int operation, int value);
    int FUN_0044ddc0(int value, unsigned char result);
};

struct ActorWeaponAccess {
    void FUN_00884f80();
};

struct WeaponDrawProcess : MiddleHighProcess {
    void FUN_00915d60(Actor* actor, bool drawn);
};

void WeaponDrawProcess::FUN_00915d60(Actor* actor, bool drawn)
{
    if (bWeaponDrawn != drawn) {
        bWeaponDrawn = drawn;
        if (actor && !bWeaponDrawn) {
            ForceWeaponDrawnSheathed(
                bWeaponDrawn,
                reinterpret_cast<BipedAnim*>(actor->GetValidBip01Names()),
                reinterpret_cast<Animation*>(actor->GetAnimData()),
                actor);
        }
    }

    if (actor && actor != DAT_011dea3c && bWeaponDrawn && pWeapon) {
        typedef void (__thiscall *WeaponChangeCallback)(Actor*, int);
        reinterpret_cast<WeaponChangeCallback>((*reinterpret_cast<void***>(actor))[0xfb])(
            actor,
            reinterpret_cast<WeaponEquipmentAccess*>(pWeapon)->FUN_0044ddc0(
                0, reinterpret_cast<WeaponEquipmentAccess*>(pWeapon)->FUN_004bda70(2, 0)));
    }

    reinterpret_cast<ActorWeaponAccess*>(actor)->FUN_00884f80();
}
