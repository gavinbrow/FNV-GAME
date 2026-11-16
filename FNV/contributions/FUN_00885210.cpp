
class ReferenceCoordinates_00885210 : public TESForm {
public:
    virtual void Unk_4E(); virtual void Unk_4F(); virtual void Unk_50();
    virtual void Unk_51(); virtual bool CastShadows(); virtual void Unk_53();
    virtual void Unk_54(); virtual void Unk_55(); virtual void Unk_56();
    virtual void Unk_57(); virtual void Unk_58(); virtual void Unk_59();
    virtual void Unk_5A(); virtual void Unk_5B(); virtual void Unk_5C();
    virtual void Unk_5D(); virtual void Unk_5E();
    virtual TESObjectREFR* RemoveItem(TESForm*, ExtraDataList*, unsigned int,
        unsigned int, unsigned int, TESObjectREFR*, unsigned int,
        unsigned int, unsigned int, unsigned char);
    virtual void Unk_60(); virtual void Unk_61(); virtual void Unk_62();
    virtual void Unk_63(); virtual void AddItem(TESForm*, ExtraDataList*, unsigned int);
    virtual void Unk_65(); virtual void Unk_66(); virtual void Unk_67();
    virtual bool GetIsChildSize(bool);
    virtual unsigned int GetActorUnk0148(); virtual void SetActorUnk0148(unsigned int);
    virtual void Unk_6B(); virtual void Unk_6C(); virtual void Unk_6D();
    virtual void Unk_6E(); virtual void Unk_6F(); virtual void Unk_70();
    virtual void AnimateNiNode(); virtual void GenerateNiNode(bool);
    virtual void Set3D(NiNode*, bool); virtual NiNode* GetNiNode();
    virtual void Unk_75();
    virtual NiPoint3 Unk_76();
    virtual NiPoint3 Unk_77();
};
float __fastcall FUN_00567400(Actor*);
void __fastcall FUN_008852b0(BaseProcess*, float);

class FUN_00885210_shell : public CachedValuesOwner {
public:
    float FUN_00885210();
};

float FUN_00885210_shell::FUN_00885210()
{
    float upper = 0.0f;
    NiPoint3 lower = reinterpret_cast<ReferenceCoordinates_00885210*>(
        reinterpret_cast<Actor*>(reinterpret_cast<char*>(this) - 0xa8))->Unk_77();
    NiPoint3 radius = reinterpret_cast<ReferenceCoordinates_00885210*>(
        reinterpret_cast<Actor*>(reinterpret_cast<char*>(this) - 0xa8))->Unk_76();
    upper = lower.y - radius.y;
    upper *= FUN_00567400(reinterpret_cast<Actor*>(reinterpret_cast<char*>(this) - 0xa8));
    if ((*reinterpret_cast<Actor*>(reinterpret_cast<char*>(this) - 0xa8)).pCurrentProcess) {
        if (FUN_00884920(reinterpret_cast<int*>(
            (*reinterpret_cast<Actor*>(reinterpret_cast<char*>(this) - 0xa8)).pCurrentProcess))) {
            FUN_008852b0((*reinterpret_cast<Actor*>(reinterpret_cast<char*>(this) - 0xa8)).pCurrentProcess, upper);
        }
    }
    return upper;
}
