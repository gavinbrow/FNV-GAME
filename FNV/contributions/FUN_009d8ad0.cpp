struct TESForm { virtual ~TESForm(); };
class TESObjectREFR : public TESForm {};
extern "C" TESForm* __cdecl FUN_004839c0(unsigned int formID);
struct MoveContext { void* FUN_008b3820(); };
struct CommandTarget { unsigned int unk00; void FUN_0066b0d0(void* target); };
struct ProcedureController {
    unsigned int unk00, unk04, unk08, unk0C, unk10, unk14, unk18, unk1C, unk20, unk24, unk28, unk2C, unk30, unk34;
    unsigned int currentForm;
    unsigned int unk3C, unk40, unk44, unk48, unk4C, unk50, unk54;
    CommandTarget command;
    unsigned char refresh;
    MoveContext* FUN_00996de0();
    void FUN_004534f0(unsigned int);
    void FUN_009d8ad0(unsigned int);
};
void ProcedureController::FUN_009d8ad0(unsigned int value)
{
    MoveContext* context = FUN_00996de0();
    FUN_004534f0(value);
    currentForm = (unsigned int)(currentForm ? dynamic_cast<TESObjectREFR*>(FUN_004839c0(currentForm)) : 0);
    if (refresh)
        command.FUN_0066b0d0(context->FUN_008b3820());
}