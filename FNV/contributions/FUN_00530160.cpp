extern char _DAT_011862b8;
extern "C" void* __cdecl FUN_00401460(void*, const void*, unsigned int);
extern "C" void __fastcall FUN_0052ed90(TESImageSpaceModifier*);
struct PassPtr { TESImageSpaceModifier* value; };
extern "C" void __fastcall FUN_004851b0(TESImageSpaceModifier*, PassPtr);
struct CopyBaseShell { void FUN_004851b0(TESImageSpaceModifier*); };
struct TESImageSpaceModifierCopy : TESImageSpaceModifier { void FUN_00530160(TESForm*); };
void TESImageSpaceModifierCopy::FUN_00530160(TESForm* form) {
  unsigned int count;
  TESImageSpaceModifier* source = (TESImageSpaceModifier*)FUN_00ec43fb(form,0,&_DAT_01183028,&_DAT_011862b8,0);
  if (!source) return;
    FUN_0052ed90(source);
    FUN_004851b0(this, *(PassPtr*)&source);
    ClearData();
    pIntroSound = source->pIntroSound;
    pOutroSound = source->pOutroSound;
    FUN_00401460(&Data,&source->Data,sizeof(Data));
    count = Data.uiBlurKeySize;
    pBlurFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pBlurFloatKey, source->pBlurFloatKey, count * sizeof(NiLinFloatKey));
    BlurInterpolator.ReplaceKeys(pBlurFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiDoubleKeySize;
    pDoubleFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pDoubleFloatKey, source->pDoubleFloatKey, count * sizeof(NiLinFloatKey));
    DoubleInterpolator.ReplaceKeys(pDoubleFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiTintColorKeySize;
    pTintColorKey = new NiLinColorKey[count];
    FUN_00401460(pTintColorKey, source->pTintColorKey, count * sizeof(NiLinColorKey));
    TintColorInterpolator.ReplaceKeys(pTintColorKey, count, NiAnimationKey::LINKEY);
    count = Data.uiFadeColorKeySize;
    pFadeColorKey = new NiLinColorKey[count];
    FUN_00401460(pFadeColorKey, source->pFadeColorKey, count * sizeof(NiLinColorKey));
    FadeColorInterpolator.ReplaceKeys(pFadeColorKey, count, NiAnimationKey::LINKEY);
    count = Data.uiRadialBlurStrengthKeySize;
    pRadialBlurStrengthFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pRadialBlurStrengthFloatKey, source->pRadialBlurStrengthFloatKey, count * sizeof(NiLinFloatKey));
    RadialBlurStrengthInterpolator.ReplaceKeys(pRadialBlurStrengthFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiRadialBlurRampupKeySize;
    pRadialBlurRampupFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pRadialBlurRampupFloatKey, source->pRadialBlurRampupFloatKey, count * sizeof(NiLinFloatKey));
    RadialBlurRampupInterpolator.ReplaceKeys(pRadialBlurRampupFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiRadialBlurStartKeySize;
    pRadialBlurStartFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pRadialBlurStartFloatKey, source->pRadialBlurStartFloatKey, count * sizeof(NiLinFloatKey));
    RadialBlurStartInterpolator.ReplaceKeys(pRadialBlurStartFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiRadialBlurRampDownKeySize;
    pRadialBlurRampDownFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pRadialBlurRampDownFloatKey, source->pRadialBlurRampDownFloatKey, count * sizeof(NiLinFloatKey));
    RadialBlurRampDownInterpolator.ReplaceKeys(pRadialBlurRampDownFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiRadialBlurDownStartKeySize;
    pRadialBlurDownStartFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pRadialBlurDownStartFloatKey, source->pRadialBlurDownStartFloatKey, count * sizeof(NiLinFloatKey));
    RadialBlurDownStartInterpolator.ReplaceKeys(pRadialBlurDownStartFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiDepthOfFieldStrengthKeySize;
    pDepthOfFieldStrengthFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pDepthOfFieldStrengthFloatKey, source->pDepthOfFieldStrengthFloatKey, count * sizeof(NiLinFloatKey));
    DepthOfFieldStrengthInterpolator.ReplaceKeys(pDepthOfFieldStrengthFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiDepthOfFieldDistanceKeySize;
    pDepthOfFieldDistanceFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pDepthOfFieldDistanceFloatKey, source->pDepthOfFieldDistanceFloatKey, count * sizeof(NiLinFloatKey));
    DepthOfFieldDistanceInterpolator.ReplaceKeys(pDepthOfFieldDistanceFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiDepthOfFieldRangeKeySize;
    pDepthOfFieldRangeFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pDepthOfFieldRangeFloatKey, source->pDepthOfFieldRangeFloatKey, count * sizeof(NiLinFloatKey));
    DepthOfFieldRangeInterpolator.ReplaceKeys(pDepthOfFieldRangeFloatKey, count, NiAnimationKey::LINKEY);
    count = Data.uiMotionBlurStrengthKeySize;
    pMotionBlurStrengthFloatKey = new NiLinFloatKey[count];
    FUN_00401460(pMotionBlurStrengthFloatKey, source->pMotionBlurStrengthFloatKey, count * sizeof(NiLinFloatKey));
    MotionBlurStrengthInterpolator.ReplaceKeys(pMotionBlurStrengthFloatKey, count, NiAnimationKey::LINKEY);
    {
    int j;
    for (int i = 0; i < 21; ++i) {
      for (j = 0; j < 2; ++j) {
        count = Data.ppuiKeySize[i][j];
        pppFloatKey[i][j] = new NiLinFloatKey[count];
        FUN_00401460(pppFloatKey[i][j],source->pppFloatKey[i][j],count * sizeof(NiLinFloatKey));
        ppInterpolator[i][j].ReplaceKeys(pppFloatKey[i][j],count,NiAnimationKey::LINKEY);
      }
    }
    }
}