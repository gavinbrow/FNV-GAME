struct FUN_00499080_shell : public Animation {
    void FUN_00499080();
};

struct ControllerManagerSequences {
    NiControllerSequence* FUN_00495d20(unsigned int index);
};
unsigned int __fastcall FUN_00495d00(NiControllerManager* manager);
void __fastcall FUN_004efa50(NiObject* object);
extern NiRTTI DAT_011c7d74;

void FUN_00499080_shell::FUN_00499080()
{
    if (!spManager)
        return;
    unsigned int sequenceCount = FUN_00495d00((NiControllerManager*)spManager);

    for (unsigned int index = 0; index < sequenceCount; ++index) {
        NiControllerSequence* sequence =
            ((ControllerManagerSequences*)(NiControllerManager*)spManager)->FUN_00495d20(index);
        NiObject* matchingObject = FUN_00653270(&DAT_011c7d74, (NiObject*)sequence);
        if (matchingObject) {
            FUN_004efa50(matchingObject);
        }
    }
    while (((FUN_00493830_shell*)this)->FUN_00493830()) {
        KFModel* model = kfModelList.GetItem();
        FUN_0043bac0(model);
        FUN_0043bac0(model);
        kfModelList.RemoveHead();
    }
}