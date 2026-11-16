struct FUN_00401170_shell
{
    unsigned int FUN_00401170();
};

struct FUN_00844eb0_shell
{
    void FUN_00844eb0(ReconstructFormData* apData);
};

struct FUN_00843270_shell : public BGSReconstructedForms
{
    void FUN_00843270(ReconstructFormData* apData);
};

void FUN_00843270_shell::FUN_00843270(ReconstructFormData* apData)
{
    if (!apData->pForm->GetIsReference() &&
        ((FUN_00401170_shell*)apData->pForm)->FUN_00401170() != 0x39 &&
        ((FUN_00401170_shell*)apData->pForm)->FUN_00401170() != 0x41)
    {
        ((FUN_00844eb0_shell*)&Forms1)->FUN_00844eb0(apData);
    }
    else
    {
        ((FUN_00844eb0_shell*)&Forms2)->FUN_00844eb0(apData);
    }
}
