class TESForm {
public:
    virtual ~TESForm();
};
class TESImageSpaceModifier : public TESForm {
public:
    virtual ~TESImageSpaceModifier();
};
extern TESImageSpaceModifier* DAT_011c9708;
TESForm* __cdecl FUN_004839c0(unsigned int);
TESImageSpaceModifier* __cdecl FUN_009ad630()
{
    if (DAT_011c9708 == 0) {
        DAT_011c9708 = dynamic_cast<TESImageSpaceModifier*>(FUN_004839c0(0x166));
    }
    return DAT_011c9708;
}
