#include "h_6fc6630b1764.h"
class TESGlobal {};

struct FormContext {
    virtual void Slot00();
    virtual void Slot01();
    virtual void Slot02();
    virtual void Slot03();
    virtual void Slot04();
    virtual void Slot05();
    virtual void Slot06();
    virtual void Slot07();
    virtual void Slot08();
    virtual void Slot09();
    virtual void Slot10();
    virtual void Slot11();
    virtual void Slot12();
    virtual void Slot13();
    virtual void Slot14();
    virtual void Slot15();
    virtual void Slot16();
    virtual void Slot17();
    virtual void Slot18();
    virtual void Slot19();
    virtual void Slot20();
    virtual void Slot21();
    virtual void Slot22();
    virtual void Slot23();
    virtual void Slot24();
    virtual void Slot25();
    virtual void Slot26();
    virtual void Slot27();
    virtual void Slot28();
    virtual void Slot29();
    virtual void Slot30();
    virtual void Slot31();
    virtual void Slot32();
    virtual void Slot33();
    virtual void Slot34();
    virtual void Slot35();
    virtual void Slot36();
    virtual void Slot37();
    virtual void Slot38();
    virtual void Slot39();
    virtual void Slot40();
    virtual void Slot41();
    virtual void Slot42();
    virtual void Slot43();
    virtual void Slot44();
    virtual void Slot45();
    virtual void Slot46();
    virtual void Slot47();
    virtual void Slot48();
    virtual void Slot49();
    virtual void Slot50();
    virtual void Slot51();
    virtual void Slot52();
    virtual void Slot53();
    virtual void Slot54();
    virtual void Slot55();
    virtual void Slot56();
    virtual void Slot57();
    virtual void Slot58();
    virtual void Slot59();
    virtual void Slot60();
    virtual void Slot61();
    virtual void Slot62();
    virtual void Slot63();
    virtual void Slot64();
    virtual void Slot65();
    virtual void Slot66();
    virtual void Slot67();
    virtual void Slot68();
    virtual void Slot69();
    virtual void Slot70();
    virtual void Slot71();
    virtual void Slot72();
    virtual void Slot73();
    virtual void Slot74();
    virtual void Slot75();
    virtual const char* GetDisplayName();
    TESFile* FUN_00484e60(int fileIndex);
    const char* FUN_0084e3a0();
};

struct FormTypeReader {
    unsigned int FUN_00401170();
};

void __cdecl FUN_00485d50(unsigned int* numericID, TESFile* file);
extern "C" void __cdecl FUN_005b5e40(const char* format, ...);
extern char DAT_01014168[];
extern char DAT_01014100[];

struct FUN_0040e7f0_owner {
    TESForm* primary;
    TESGlobal* secondary;
    void FUN_0040e7f0(FormContext* context);
};

void FUN_0040e7f0_owner::FUN_0040e7f0(FormContext* context)
{
    if (primary != 0) {
        unsigned int numericID = (unsigned int)primary;
        FUN_00485d50(&numericID, context->FUN_00484e60(-1));
        primary = _ref_004839c0(numericID);
        if (primary == 0) {
            FUN_005b5e40(DAT_01014168, numericID,
                         context->GetDisplayName(),
                         context->FUN_0084e3a0());
        }
    }

    if (primary != 0) {
        if (((FormTypeReader*)primary)->FUN_00401170() == 42 && secondary != 0) {
            unsigned int associatedID = (unsigned int)secondary;
            FUN_00485d50(&associatedID, context->FUN_00484e60(-1));
            secondary = dynamic_cast<TESGlobal*>(_ref_004839c0(associatedID));
            if (secondary == 0) {
                FUN_005b5e40(DAT_01014100, associatedID,
                             context->GetDisplayName(),
                             context->FUN_0084e3a0());
            }
        }
    } else {
        secondary = 0;
    }
}