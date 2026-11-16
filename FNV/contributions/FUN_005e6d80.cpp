class BGSEntryPointFunctionData {
public:
    virtual ~BGSEntryPointFunctionData();
};

class ActivateChoiceForm {
public:
    bool FUN_005ab240(ActivateChoiceForm* other);
};

class ActivateChoiceCompare : public BGSEntryPointFunctionData {
public:
    const char* choiceText;
    unsigned char formStorage[0x54];
    unsigned short flags;

    ActivateChoiceForm* FUN_00413f40();
    bool FUN_005e6d80(BGSEntryPointFunctionData* other);
};

int __cdecl FUN_00408b20(const char* lhs, const char* rhs);

bool ActivateChoiceCompare::FUN_005e6d80(BGSEntryPointFunctionData* other)
{
    ActivateChoiceCompare* choice = reinterpret_cast<ActivateChoiceCompare*>(
        dynamic_cast<BGSEntryPointFunctionDataActivateChoice*>(other));
    if (choice == 0)
        return true;
    if ((choiceText != 0 && choice->choiceText == 0) ||
        (choiceText == 0 && choice->choiceText != 0))
        return true;
    if (choiceText != 0 && choice->choiceText != 0 &&
        FUN_00408b20(choiceText, choice->choiceText))
        return true;
    if (FUN_00413f40()->FUN_005ab240(choice->FUN_00413f40()))
        return true;
    if (flags != choice->flags)
        return true;
    return false;
}
