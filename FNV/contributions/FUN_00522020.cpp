extern "C" void* __cdecl memcpy(void*, const void*, unsigned int);
extern unsigned char DAT_01183028;
extern unsigned char DAT_01183998;
TESObjectWEAP* __cdecl FUN_00ec43fb(unsigned int, unsigned int, void*, void*, unsigned int);
struct StringCopyAccess : BSStringT<char> {
    const char* FUN_00559450(bool);
    void FUN_004037f0(const char*);
};
struct StackWord { unsigned int word; };
struct WeaponCopyAccess;
extern "C" void __fastcall FUN_004851b0(WeaponCopyAccess*, StackWord);
extern "C" void* __fastcall FUN_008d8ac0(WeaponCopyAccess*);
struct WeaponCopyAccess : TESObjectWEAP {
    void FUN_00522020(unsigned int id);
    void FUN_008d8ae0(void*);
    BGSImpactDataSet* FUN_008d8b00();
    TESObjectSTAT* FUN_004ab500(unsigned char);
    TESObjectIMOD* FUN_004bd570(unsigned char);
    TESSound* FUN_00522440(bool);
    TESSound* FUN_00522470(bool);
    TESSound* FUN_008bffa0();
    TESSound* FUN_005224e0();
    TESSound* FUN_005224c0();
    TESSound* FUN_00522500();
    TESSound* FUN_00522520();
    TESSound* FUN_00522540();
    TESSound* FUN_00521630();
    TESSound* FUN_008d8a60();
    TESSound* FUN_005224a0();
    void FUN_005215f0(TESSound*);
    void FUN_005c8a30(TESSound*);
    void FUN_00521710(BGSImpactDataSet*);
    void FUN_00521610(TESSound*);
    void FUN_008d8a80(TESSound*);
    void FUN_008d8aa0(TESSound*);
    SOUND_LEVEL FUN_00522560(bool);
    unsigned int FUN_00401170();
    void FUN_004f15a0(unsigned int);
};
void WeaponCopyAccess::FUN_00522020(unsigned int id)
{
    WeaponCopyAccess* source = (WeaponCopyAccess*)FUN_00ec43fb(id, 0, &DAT_01183028, &DAT_01183998, 0);
    if (source == 0) return;
    {
        FUN_004851b0(this, *(StackWord*)&id);
        ShellCasingModel.CopyFromBase(&source->ShellCasingModel);
        ((StringCopyAccess*)&EmbeddedWeaponNode)->FUN_004037f0(
            ((StringCopyAccess*)&source->EmbeddedWeaponNode)->FUN_00559450(false));
        ((StringCopyAccess*)&VATSAttackName)->FUN_004037f0(
            ((StringCopyAccess*)&source->VATSAttackName)->FUN_00559450(false));
        WorldModel.CopyFromBase(&source->WorldModel);
        ScopeModel.CopyFromBase(&source->ScopeModel);
        FUN_0051f570(source->GetScopeEffect());
        FUN_008d8ae0(FUN_008d8ac0(source));
        FUN_00521710(source->FUN_008d8b00());
        Set1stPersonModObject(1, source->FUN_004ab500(1));
        Set1stPersonModObject(2, source->FUN_004ab500(2));
        Set1stPersonModObject(3, source->FUN_004ab500(3));
        Set1stPersonModObject(4, source->FUN_004ab500(4));
        Set1stPersonModObject(5, source->FUN_004ab500(5));
        Set1stPersonModObject(6, source->FUN_004ab500(6));
        Set1stPersonModObject(7, source->FUN_004ab500(7));
        SetModItem(1, source->FUN_004bd570(1));
        SetModItem(2, source->FUN_004bd570(2));
        SetModItem(4, source->FUN_004bd570(4));
        WorldModelMod1.CopyFromBase(&source->WorldModelMod1);
        WorldModelMod2.CopyFromBase(&source->WorldModelMod2);
        WorldModelMod3.CopyFromBase(&source->WorldModelMod3);
        WorldModelMod12.CopyFromBase(&source->WorldModelMod12);
        WorldModelMod13.CopyFromBase(&source->WorldModelMod13);
        WorldModelMod23.CopyFromBase(&source->WorldModelMod23);
        WorldModelMod123.CopyFromBase(&source->WorldModelMod123);
        memcpy(&data, &source->data, sizeof(data));
        memcpy(&criticalData, &source->criticalData, sizeof(criticalData));
        memcpy(&specialVATSData, &source->specialVATSData, sizeof(specialVATSData));
        SetAttackSound(source->GetAttackSound(false));
        FUN_005215f0(source->FUN_00522440(false));
        FUN_005c8a30(source->FUN_00522470(false));
        FUN_00521650(source->FUN_008bffa0());
        SetMeleeBlockSound(source->FUN_005224e0());
        SetAttackFailSound(source->FUN_005224c0());
        SetIdleSound(source->FUN_00522500());
        SetEquipSound(source->FUN_00522520());
        SetUnequipSound(source->FUN_00522540());
        FUN_00521610(source->FUN_00521630());
        FUN_008d8a80(source->FUN_008d8a60());
        FUN_008d8aa0(source->FUN_005224a0());
        eSoundLevel = source->FUN_00522560(false);
        FUN_004f15a0(source->FUN_00401170());
    }
}