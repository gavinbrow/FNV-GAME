
struct CompareForm : TESForm {
    bool FUN_004853e0(BaseFormComponent* rhs);
    int FUN_00474cb0();
    unsigned int FUN_0044ddc0();
};
extern "C" int __cdecl FUN_00404dc0(const char*, const char*);

bool CompareForm::FUN_004853e0(BaseFormComponent* rhs)
{
    TESForm* otherForm = dynamic_cast<TESForm*>(rhs);
    if (!otherForm)
        return true;

    if (cFormType != otherForm->GetFormType())
        return true;

    if (FUN_00474cb0() || reinterpret_cast<CompareForm*>(otherForm)->FUN_00474cb0()) {
        if (FUN_00474cb0() != reinterpret_cast<CompareForm*>(otherForm)->FUN_00474cb0())
            return true;
        else {
            if (FUN_00404dc0(GetName(), otherForm->GetName()))
                return true;
        }
    }

    unsigned int flagsA = FUN_0044ddc0();
    unsigned int flagsB = reinterpret_cast<CompareForm*>(otherForm)->FUN_0044ddc0();
    flagsA &= 0xffffbff4;
    flagsB &= 0xffffbff4;
    if (flagsA != flagsB)
        return true;
    return false;
}
