struct ScriptParameterHandler {
    int FUN_00ad56b0(
        int unusedFirst,
        int primaryValue,
        int unusedThird,
        int* primaryOutput,
        int secondaryValue,
        int unusedSixth,
        int* secondaryOutput);
};

int ScriptParameterHandler::FUN_00ad56b0(
    int unusedFirst,
    int primaryValue,
    int unusedThird,
    int* primaryOutput,
    int secondaryValue,
    int unusedSixth,
    int* secondaryOutput)
{
    *primaryOutput = primaryValue;
    *secondaryOutput = secondaryValue;
    return 3;
}