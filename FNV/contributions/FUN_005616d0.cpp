
extern float DAT_01017d00;
struct TriggerContext { int __thiscall FUN_00561730(void* result); };
struct VirtualDispatcher {
 virtual void slot00(); virtual void slot04(); virtual void slot08(); virtual void slot0C();
 virtual void slot10(); virtual void slot14(); virtual void slot18(); virtual void slot1C();
 virtual void slot20(); virtual void slot24(); virtual void slot28(); virtual void slot2C();
 virtual void slot30(); virtual void slot34(); virtual void slot38(); virtual void slot3C();
 virtual void Dispatch(TriggerContext* context);
};
struct FUN_005616d0_Owner {
 void* __thiscall FUN_00560dc0(float amount);
 void __thiscall FUN_00c9c1d0();
 VirtualDispatcher* __thiscall FUN_009d9f40();
 void __thiscall FUN_005616d0(TriggerContext* context);
};
void FUN_005616d0_Owner::FUN_005616d0(TriggerContext* context) {
 if (!context->FUN_00561730(FUN_00560dc0(DAT_01017d00))) {
 FUN_00c9c1d0();
 FUN_009d9f40()->Dispatch(context);
 }
}