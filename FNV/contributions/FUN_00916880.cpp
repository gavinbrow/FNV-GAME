
struct ActorCalls {
    int FUN_00931850();
    bool FUN_00437bf0();
    bool FUN_00437bd0();
    bool FUN_005a2030();
    bool FUN_0087f3b0();
    bool FUN_0087f570();
    bool FUN_00493bb0();
    void* FUN_005d43c0();
    float FUN_00572380(NiPoint3*);
    int FUN_008a8230(Actor*);
    void FUN_0093a690(Actor*);
    int FUN_00953c20();
};
struct PackageCalls {
    int FUN_0041ca90();
    bool FUN_00678610();
    bool FUN_0067a3f0();
    unsigned int FUN_00676280(Actor*);
};
struct ControllerCalls {
    bool FUN_0097fa10();
};
struct GlobalCallContext {
    bool FUN_008d0300(Actor*, Actor*);
};
struct TimingSettings {
    int* FUN_0043d4d0();
};
struct ProcessToken {
    void* FUN_0041cb10();
};
extern GlobalCallContext* DAT_011f1958;
extern TimingSettings DAT_011ccffc;
extern Actor* DAT_011dea3c;
extern float DAT_01012054;
extern double DAT_01012070;
extern float DAT_0101786c;

typedef bool (__thiscall *PackageFilter)(TESPackage*, Actor*, Actor*, int, float, int);
typedef ControllerCalls* (__thiscall *ControllerForTarget)(Actor*, Actor*);
typedef void (__thiscall *ImmediateAction)(Actor*, Actor*, int, int, int, int, int, float, float);
typedef void (__thiscall *ProcessAction)(Actor*, Actor*, int, bool, bool, bool, int, bool, int);

struct FUN_00916880_shell : MiddleHighProcess {
    void FUN_0090dc10(Actor*, Actor*, bool, bool, int, bool, bool, bool, bool, bool, int, int, int);
    bool FUN_00916880(Actor*, Actor*, bool, bool, int, bool, bool, bool, bool, bool, bool, bool, int);
};

bool FUN_00916880_shell::FUN_00916880(
    Actor* actor, Actor* target, bool deferAction, bool secondaryAction,
    int movementOption, bool optionA, bool optionB, bool optionC,
    bool optionD, bool stopReason, bool skipDistanceCheck,
    bool extraOption, int callbackValue)
{
    if (GetFinishingCombatPackage())
        return false;
    TESPackage* pkg = GetCurrentPackage();
    if (!deferAction && pkg &&
        reinterpret_cast<PackageCalls*>(pkg)->FUN_0041ca90() == 9 &&
        !reinterpret_cast<PackageFilter>(
            (*reinterpret_cast<void***>(pkg))[0x140 / 4])
            (pkg, target, actor, 0, DAT_01012054, 0))
        return false;

    if (target == 0 && movementOption == 0) {
        reinterpret_cast<ProcessAction>((*reinterpret_cast<void***>(actor))[0x424 / 4])
            (actor, 0, 0, 0, 0, 0, 0, 0, callbackValue);
        }
    else {
    if (target) {
        if (reinterpret_cast<ActorCalls*>(target)->FUN_00931850() !=
            reinterpret_cast<ActorCalls*>(actor)->FUN_00931850() &&
            actor->GetNiNode() == 0)
            FUN_0090dc10(actor, target, deferAction, secondaryAction, movementOption,
                optionA, optionB, optionC, optionD, skipDistanceCheck, 0, 1, 0);
    }

    if (reinterpret_cast<ActorCalls*>(actor)->FUN_00437bf0() ||
        reinterpret_cast<ActorCalls*>(actor)->FUN_00437bd0())
        return false;

    if (target && !actor->GetCombatController() && !stopReason &&
        DAT_011f1958->FUN_008d0300(actor, target)) {
        reinterpret_cast<ImmediateAction>((*reinterpret_cast<void***>(actor))[0x410 / 4])
            (actor, target, 1, 1, 1, 0, 0, DAT_01012054, DAT_01012054);
        if (target == DAT_011dea3c &&
            reinterpret_cast<ActorCalls*>(DAT_011dea3c)->FUN_008a8230(actor) > 0)
            reinterpret_cast<ActorCalls*>(DAT_011dea3c)->FUN_0093a690(actor);
        return true;
    }

    if (actor->GetCombatController() && target && movementOption == 0 &&
        reinterpret_cast<ControllerCalls*>(reinterpret_cast<ControllerForTarget>((*reinterpret_cast<void***>(actor))[0x428 / 4])(actor, target))->FUN_0097fa10())
        return false;

    if (target == DAT_011dea3c && !stopReason) {
        if (reinterpret_cast<ActorCalls*>(DAT_011dea3c)->FUN_00953c20() >=
            *DAT_011ccffc.FUN_0043d4d0())
            return false;
    }

    if (target) {
        bool hasCondition = reinterpret_cast<ActorCalls*>(target)->FUN_005a2030();
        if (!reinterpret_cast<ActorCalls*>(actor)->FUN_0087f3b0() && hasCondition)
            return false;
        if (reinterpret_cast<ActorCalls*>(actor)->FUN_0087f570() && !hasCondition)
            return false;
    }

    ClearMovementStoped();
    TESPackage* runningPackage = GetPackageThatIsRunning();
    if (runningPackage &&
        reinterpret_cast<PackageCalls*>(runningPackage)->FUN_00678610())
        runningPackage = reinterpret_cast<TESPackage*>(
            reinterpret_cast<ProcessToken*>(
                reinterpret_cast<ActorCalls*>(actor)->FUN_005d43c0())->FUN_0041cb10());

    if (target && runningPackage &&
        reinterpret_cast<PackageCalls*>(runningPackage)->FUN_0067a3f0() &&
        !stopReason && !skipDistanceCheck) {
        NiPoint3 destination = GetCurrentDestinationCoordinate(actor, false);
        float radius = static_cast<float>(
            reinterpret_cast<PackageCalls*>(runningPackage)->FUN_00676280(actor));
        if (radius < DAT_01012070)
            radius = DAT_0101786c;
        if (radius < reinterpret_cast<ActorCalls*>(target)->FUN_00572380(&destination)
            && target->GetCombatController()
            && !reinterpret_cast<ControllerCalls*>(reinterpret_cast<ControllerForTarget>((*reinterpret_cast<void***>(target))[0x428 / 4])(target, actor))->FUN_0097fa10()) {
            SetDetectAlert(true);
            return false;
        }
    }

    if (!actor->GetCombatController()) {
        SetDetectAlert(false);
        actor->Unk_A2();
        pSavedAcquireObject = pAcquireObject;
        pAcquireObject = 0;
    }
    bool isAggressor = optionC;
    if (actor->Unk_C1())
        isAggressor = false;
    if (target && reinterpret_cast<ActorCalls*>(target)->FUN_00493bb0()
        && target->GetCombatController()
        && reinterpret_cast<ControllerCalls*>(reinterpret_cast<ControllerForTarget>((*reinterpret_cast<void***>(target))[0x428 / 4])(target, actor))->FUN_0097fa10())
        isAggressor = false;
    SetIsAggressor(isAggressor);

    int timedStop = 0;
    if (stopReason)
        timedStop = 200;
    reinterpret_cast<ProcessAction>((*reinterpret_cast<void***>(actor))[0x424 / 4])
        (actor, target, movementOption, stopReason, isAggressor,
            optionA, timedStop, extraOption, callbackValue);

    if (target == DAT_011dea3c &&
        reinterpret_cast<ActorCalls*>(actor)->FUN_00493bb0() &&
        reinterpret_cast<ActorCalls*>(DAT_011dea3c)->FUN_008a8230(actor) > 0)
        reinterpret_cast<ActorCalls*>(DAT_011dea3c)->FUN_0093a690(actor);
}
    return true;
}
