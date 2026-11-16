struct ScriptArgs;
struct ScriptState;
struct ExecutionContext;
struct EventVars;
struct Reference;
struct GameFlags {
    void FUN_005d14d0(bool value);
    void FUN_005d1590(bool value);
    void FUN_005d1530(bool value);
};
extern GameFlags* DAT_011dea3c;
bool __cdecl FUN_005accb0(
    const ScriptArgs* parameters,
    const char* source,
    unsigned int& offset,
    Reference* actor,
    Reference* container,
    ScriptState* script,
    EventVars* variables,
    int* secondFlag,
    int* thirdFlag,
    int* firstFlag);
bool __cdecl FUN_005d13e0(
    const ScriptArgs* parameters,
    const char* source,
    Reference* actor,
    Reference* container,
    ScriptState* script,
    EventVars* variables,
    double& result,
    unsigned int& offset)
{
    int secondFlag = 0;
    int thirdFlag = 1;
    int firstFlag = 0;
    if (!FUN_005accb0(parameters, source, offset, actor, container,
                     script, variables, &secondFlag, &thirdFlag, &firstFlag))
        return false;
    if (secondFlag == 0) {
        DAT_011dea3c->FUN_005d14d0(false);
        if (thirdFlag == 0)
            DAT_011dea3c->FUN_005d1590(false);
        else
            DAT_011dea3c->FUN_005d1590(true);
        if (firstFlag == 1)
            DAT_011dea3c->FUN_005d1530(true);
    } else {
        DAT_011dea3c->FUN_005d14d0(true);
        DAT_011dea3c->FUN_005d1590(true);
        if (firstFlag == 1)
            DAT_011dea3c->FUN_005d1530(true);
        else
            DAT_011dea3c->FUN_005d1530(false);
    }
    return true;
}
