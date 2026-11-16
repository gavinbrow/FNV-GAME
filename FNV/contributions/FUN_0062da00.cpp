struct TESObjectREFR;
TESObjectREFR* __cdecl FUN_0062b4e0(void* object);
struct EventContext {void* FUN_0043b540();};
struct InputBody {EventContext* FUN_00460140();};
struct EventCode {int value;void FUN_008c71b0(void* rawCode);int FUN_0043b4d0();};
struct TrapEventHandler {void FUN_00576800(TESObjectREFR* reference);void FUN_00620130(TESObjectREFR* reference);};
struct FUN_0062da00_Class {void FUN_0062da00(InputBody* source);};
void FUN_0062da00_Class::FUN_0062da00(InputBody* source) {
    EventContext* resolvedBody = source->FUN_00460140();
    EventCode notification;
    notification.FUN_008c71b0(resolvedBody->FUN_0043b540());
    int category = notification.FUN_0043b4d0();
    if (category == 14 || category == 16 || category == 30) {
        TESObjectREFR* reference = FUN_0062b4e0(resolvedBody);
        if (reference != 0) {
            if (category == 14 || category == 16) {
                reinterpret_cast<TrapEventHandler*>(reinterpret_cast<char*>(this) - 8)->FUN_00576800(reference);
            } else {
                reinterpret_cast<TrapEventHandler*>(reinterpret_cast<char*>(this) - 8)->FUN_00620130(reference);
            }
        }
    }
}