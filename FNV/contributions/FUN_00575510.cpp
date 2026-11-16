struct TESContainer;
TESContainer* __fastcall FUN_0055d310(TESObjectREFR* reference);
struct SelectedObject {};
struct ObjectProvider {};
extern "C" ObjectProvider* DAT_011c3f2c;
extern "C" SelectedObject* __fastcall FUN_00740960(ObjectProvider* provider);
extern "C" void* __fastcall FUN_004ca200(SelectedObject* selected);
extern "C" SelectedObject* __cdecl FUN_004bf220(TESObjectREFR* reference);
struct FUN_00575510_shell : TESObjectREFR {
    void FUN_00575510(bool useProvider, void** relatedObject, SelectedObject** selectedObject);
};
void FUN_00575510_shell::FUN_00575510(bool useProvider, void** relatedObject, SelectedObject** selectedObject)
{
    TESContainer* container;
    SelectedObject* resolvedSelection = 0;
    container = FUN_0055d310(this);
    *selectedObject = 0;
    *relatedObject = 0;
    if (container) {
        if (useProvider) {
            *selectedObject = FUN_00740960(DAT_011c3f2c);
        } else {
            *selectedObject = FUN_004bf220(this);
        }
        *relatedObject = FUN_004ca200(*selectedObject);
    }
}