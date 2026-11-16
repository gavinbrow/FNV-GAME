
void __cdecl FUN_005293f0(void*);
void __cdecl FUN_0083e510();
struct FUN_00761960 : Menu {
    DialogMenu::DialogState eDialogState;
    DialogMenu::GoodbyeState eGoodbyeState;
    Tile* pTiles[4];
    ListBox_int_ lbResponseList;
    MenuTopicManager* pTopicManager;
    BSSoundHandle hSpeechFile;
    MobileObject* pSpeaker;
    char strCurrTopicID[128];
    bool bResponseShown;
    unsigned char layoutPadding105[3];
    float fElapsedSecs;
    unsigned int uiIgnoreInputStartTime;
    DialogMenuPoint2 DOFDepth, DOFRange, DOFStrength;
    float fPercentZoomed;
    ImageSpaceModifierInstanceDOF* pDepthOfFieldInstance;
    bool bIsIn3rdPerson, bPaused;
    unsigned char layoutPadding132[2];
    DialogMenu::DialogState ePausedState;
    bool bInServiceMenu, bShowingTutorial, bDoServiceLoad;
    unsigned char layoutPadding13B[1];
    ~FUN_00761960();
};
FUN_00761960::~FUN_00761960() {
    DAT_011d9514 = false;
    if (DAT_011d9510->pDepthOfFieldInstance) {
        FUN_005293f0(pDepthOfFieldInstance);
        pDepthOfFieldInstance = 0;
    }
    FUN_0083e510();
    DAT_011d9510 = 0;
}
