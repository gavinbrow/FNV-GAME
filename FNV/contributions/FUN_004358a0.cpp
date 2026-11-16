struct ExtraMember {
    ExtraMember(int initial);
    ~ExtraMember();
    void Reset(int value);
};

class FUN_004358a0 : public BSExtraData {
public:
    ExtraMember member;
    FUN_004358a0();
    virtual ~FUN_004358a0();
};

FUN_004358a0::FUN_004358a0() : BSExtraData(0x79), member(0)
{
    member.Reset(0);
}