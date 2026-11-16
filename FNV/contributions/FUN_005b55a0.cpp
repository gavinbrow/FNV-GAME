struct PerkTarget { float FUN_004ce340(TESObjectREFR* ref, int first, bool unusedA, bool hasSecond, bool unusedB, bool hasThird, int fourth, int fifth); };
struct ScriptTargetBase { PerkTarget* FUN_00418520(); };
struct ScriptReference { ScriptTargetBase* FUN_005d43c0(); };
struct ActorUpdateQueue { void FUN_00952c30(TESObjectREFR* reference); };
extern ActorUpdateQueue* DAT_011dea3c;
bool __cdecl FUN_005b55a0(const SCRIPT_PARAMETER* args, const char* raw, TESObjectREFR* reference, TESObjectREFR* other, Script* script, ScriptLocals* locals, double& result, unsigned int& offset)
{
    int firstValue = 0;
    int secondArgument = 0;
    int thirdValue = 0;
    int fourthOutput = -1;
    int fifthInput = 0;
    if (!ExtractArgs(args, raw, &offset, reference, other, script, locals, &firstValue, &secondArgument, &thirdValue, &fourthOutput, &fifthInput))
        return false;
    bool hasSecondValue = false;
    if (secondArgument != 0)
        hasSecondValue = true;
    if (reference && reinterpret_cast<ScriptReference*>(reference)->FUN_005d43c0())
    {
        PerkTarget* target = reinterpret_cast<ScriptReference*>(reference)->FUN_005d43c0()->FUN_00418520();
        if (target)
        {
            target->FUN_004ce340(reference, firstValue, false, hasSecondValue, false, thirdValue != 0, fourthOutput, fifthInput);
            DAT_011dea3c->FUN_00952c30(reference);
        }
    }
    return true;
}