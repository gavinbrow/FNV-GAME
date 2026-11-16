class S2 { public: void* FUN_00a532d0(int value); };
class NiBoolInterpControllerShim : public NiBoolInterpController {
public:
    NiInterpolator* FUN_00a57710(int unused);
};
NiInterpolator* NiBoolInterpControllerShim::FUN_00a57710(int unused)
{
    union BoolWord { bool flag; int word; } value;
    GetPoseValue(value.flag);
    S2* result = (S2*)BSFadeNode::operator new(0x18);
    if (result)
        return (NiInterpolator*)result->FUN_00a532d0(value.word);
    return 0;
}
