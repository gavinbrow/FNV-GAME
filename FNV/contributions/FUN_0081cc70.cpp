class FUN_0081cc70_refvt {
public:
    virtual void s000();
    virtual void s001();
    virtual void s002();
    virtual void s003();
    virtual void s004();
    virtual void s005();
    virtual void s006();
    virtual void s007();
    virtual void s008();
    virtual void s009();
    virtual void s010();
    virtual void s011();
    virtual void s012();
    virtual void s013();
    virtual void s014();
    virtual void s015();
    virtual void s016();
    virtual void s017();
    virtual void s018();
    virtual void s019();
    virtual void s020();
    virtual void s021();
    virtual void s022();
    virtual void s023();
    virtual void s024();
    virtual void s025();
    virtual void s026();
    virtual void s027();
    virtual void s028();
    virtual void s029();
    virtual void s030();
    virtual void s031();
    virtual void s032();
    virtual void s033();
    virtual void s034();
    virtual void s035();
    virtual void s036();
    virtual void s037();
    virtual void s038();
    virtual void s039();
    virtual void s040();
    virtual void s041();
    virtual void s042();
    virtual void s043();
    virtual void s044();
    virtual void s045();
    virtual void s046();
    virtual void s047();
    virtual void s048();
    virtual void s049();
    virtual void s050();
    virtual void s051();
    virtual void s052();
    virtual void s053();
    virtual void s054();
    virtual void s055();
    virtual void s056();
    virtual void s057();
    virtual void s058();
    virtual void s059();
    virtual void s060();
    virtual void s061();
    virtual void s062();
    virtual void s063();
    virtual void s064();
    virtual void s065();
    virtual void s066();
    virtual void s067();
    virtual void s068();
    virtual void s069();
    virtual void s070();
    virtual void s071();
    virtual void s072();
    virtual void s073();
    virtual void s074();
    virtual void s075();
    virtual void s076();
    virtual void s077();
    virtual void s078();
    virtual void s079();
    virtual void s080();
    virtual void s081();
    virtual void s082();
    virtual void s083();
    virtual void s084();
    virtual void s085();
    virtual void s086();
    virtual void s087();
    virtual void s088();
    virtual void s089();
    virtual void s090();
    virtual void s091();
    virtual void s092();
    virtual void s093();
    virtual void s094();
    virtual void s095();
    virtual void s096();
    virtual void s097();
    virtual void s098();
    virtual void s099();
    virtual void s100();
    virtual void s101();
    virtual void s102();
    virtual void s103();
    virtual void s104();
    virtual void s105();
    virtual void s106();
    virtual void s107();
    virtual void s108();
    virtual void s109();
    virtual void s110();
    virtual void s111();
    virtual void s112();
    virtual void s113();
    virtual void s114();
    virtual void s115();
    virtual int s116();
};
class FUN_0081cc70_thisvt {
public:
    virtual void s000();
    virtual void s001();
    virtual void s002();
    virtual void s003();
    virtual void s004();
    virtual void s005();
    virtual void s006();
    virtual void s007();
    virtual void s008();
    virtual void s009();
    virtual void s010();
    virtual void s011();
    virtual void s012();
    virtual void s013();
    virtual void s014();
    virtual void s015();
    virtual void s016();
    virtual void s017();
    virtual void s018();
    virtual void s019();
    virtual void s020();
    virtual void s021();
    virtual void s022();
    virtual void s023();
    virtual void s024();
    virtual void s025();
    virtual void s026();
    virtual void s027();
    virtual void s028();
    virtual void s029();
    virtual void s030();
    virtual void s031();
    virtual void s032();
    virtual void s033();
    virtual void s034();
    virtual void s035();
    virtual void s036();
    virtual void s037();
    virtual void s038();
    virtual void s039();
    virtual void s040();
    virtual void s041();
    virtual void s042();
    virtual void s043();
    virtual void s044();
    virtual void s045();
    virtual void s046();
    virtual void s047();
    virtual void s048();
    virtual void s049();
    virtual void s050();
    virtual void s051();
};
class FUN_0081cc70_seqvt {
public:
    virtual void s000();
    virtual void s001();
    virtual void s002();
    virtual void s003();
    virtual void s004();
    virtual void s005();
    virtual void s006();
    virtual void s007();
    virtual void s008();
    virtual void s009();
    virtual void s010();
    virtual void s011();
    virtual void s012();
    virtual void s013();
    virtual void s014();
    virtual void s015();
    virtual void s016();
    virtual void s017();
    virtual void s018();
    virtual void s019();
    virtual void s020();
    virtual void s021();
    virtual void s022();
    virtual void s023();
    virtual void s024();
    virtual void s025();
    virtual void s026();
    virtual void s027();
    virtual void s028();
    virtual void s029();
    virtual void s030();
    virtual void s031();
    virtual void s032();
    virtual void s033();
    virtual void s034();
    virtual void s035(float, bool);
};

struct FUN_0081cc70_helper {
    NiAVObject* FUN_00559450();
};

struct FUN_0081cc70_helper2 {
    NiProperty* FUN_0043b230();
};

struct FUN_0081cc70_seqm {
    float FUN_00508120();
    float FUN_00508100();
    int FUN_008041a0();
    int FUN_0059bb30();
};

class FUN_0081cc70_cls : public MagicModelHitEffect {
public:
    bool FUN_0081b860(float afTime);
    bool FUN_0081cc70(float afTime);
};

bool FUN_0081cc70_cls::FUN_0081cc70(float afTime) {
    if (pTarget == 0 || ((FUN_0081cc70_refvt*)pTarget)->s116() == 0 || !FUN_0081b860(afTime)) {
        return false;
    }
    if (((FUN_0081cc70_helper*)&spObject)->FUN_00559450() != 0) {
        ((FUN_0081cc70_thisvt*)this)->s051();
        SkyShaderProperty* prop = FUN_00653270(&DAT_011f36ac, ((FUN_0081cc70_helper2*)((FUN_0081cc70_helper*)&spObject)->FUN_00559450())->FUN_0043b230());
        if (prop != 0) {
            NiControllerSequence* seq = ((NiControllerManager*)prop)->GetSequenceByName(NiFixedString("SpecialIdle_HitEffect"));
            if (seq != 0) {
                if (((FUN_0081cc70_seqm*)seq)->FUN_00508100() > ((FUN_0081cc70_seqm*)seq)->FUN_00508120() && ((FUN_0081cc70_seqm*)seq)->FUN_008041a0()) {
                    if (((FUN_0081cc70_seqm*)seq)->FUN_0059bb30() == 2 || bFinished != 0) {
                        bFinished = 1;
                        ((FUN_0081cc70_seqvt*)seq)->s035(0.0f, false);
                        fLifetime = fAge;
                    }
                }
            }
        }
    }
    if (bFinished != 0) {
        if ((double)fLifetime + 2.0 < fAge) {
            return false;
        }
    }
    return true;
}
