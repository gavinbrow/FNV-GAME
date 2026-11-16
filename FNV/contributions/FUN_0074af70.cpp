struct UIWidget { virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03(); virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07(); virtual void v08(); virtual void v09(); virtual void v0a(); virtual void v0b(); virtual void v0c(); virtual void v0d(); virtual void v0e(); virtual void v0f(); virtual void v10(); virtual void v11(); virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15(); virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19(); virtual void v1a(); virtual void v1b(); virtual void v1c(); virtual void v1d(); virtual void v1e(); virtual void v1f(); virtual void v20(); virtual void v21(); virtual void v22(); virtual void v23(); virtual void v24(); virtual void v25(); virtual void v26(); virtual void v27(); virtual void v28(); virtual void v29(); virtual void v2a(); virtual void v2b(); virtual void v2c(); virtual void v2d(); virtual void v2e(); virtual void v2f(); virtual void v30(); virtual void v31(); virtual void v32(); virtual void v33(); virtual void v34(); virtual void v35(); virtual void v36(); virtual void v37(); virtual void v38(); virtual void v39(); virtual void v3a(); virtual void v3b(); virtual void SetResource(int,int,unsigned int); };

struct UIAssetName { const char* FUN_00408da0(); };
struct UIAssetSource {
    bool FUN_0073cb80();
    UIAssetName* FUN_0050d100();
    UIAssetName* FUN_00503650();
};
struct UIAssetChain { UIAssetSource** FUN_006a7ad0(int); };
struct UIMenuManager { void FUN_004568c0(char*,GO*,int,int); };
struct UIOptions { void FUN_00a011b0(int); };
extern "C" UIMenuManager* DAT_011dea10;
extern char UNK_0101996c, UNK_0101d7fc;
extern "C" int __cdecl FUN_00ec62c0();
extern "C" void __cdecl FUN_00406d00(char*,unsigned int,const char*,const char*,const char*);
extern "C" void __cdecl FUN_004b7240(char*,char*,unsigned int);
struct HudGlyphMenu {
    void FUN_0074af70(int iconIndex);
};
void HudGlyphMenu::FUN_0074af70(int iconIndex) {
    if (*(void**)((char*)this+0x91c) &&
        *(void**)((char*)this+0x97c) &&
        *(void**)((char*)this+0x9dc) &&
        *(void**)((char*)this+0xa3c)) {
        (*(UIOptions**)((char*)this+0x6c))->FUN_00a011b0(DAT_011d9170);
        int imageKey = FUN_00ec62c0();
        char generatedPath[260];
        char resolvedPath[260];
        if ((*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_0073cb80()) {
            GO currentIcon(0);

            FUN_00406d00(generatedPath,260,&UNK_0101996c,&UNK_0101d7fc,
                 (*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_0050d100()->FUN_00408da0());
            FUN_004b7240(generatedPath,resolvedPath,260);
            DAT_011dea10->FUN_004568c0(resolvedPath,&currentIcon,0,0);
            if ((unsigned int)currentIcon != 0) {
                ((UIWidget*)*(void**)((char*)this+iconIndex*4+0x8ec))->SetResource(0,0,(unsigned int)currentIcon);
            }

            FUN_00406d00(generatedPath,260,&UNK_0101996c,&UNK_0101d7fc,
                 (*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_00503650()->FUN_00408da0());
            FUN_004b7240(generatedPath,resolvedPath,260);
            DAT_011dea10->FUN_004568c0(resolvedPath,&currentIcon,0,0);
            if ((unsigned int)currentIcon != 0) {
                ((UIWidget*)*(void**)((char*)this+iconIndex*4+0x94c))->SetResource(0,0,(unsigned int)currentIcon);
            }

            FUN_00406d00(generatedPath,260,&UNK_0101996c,&UNK_0101d7fc,
                 (*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_00503650()->FUN_00408da0());
            FUN_004b7240(generatedPath,resolvedPath,260);
            DAT_011dea10->FUN_004568c0(resolvedPath,&currentIcon,0,0);
            if ((unsigned int)currentIcon != 0) {
                ((UIWidget*)*(void**)((char*)this+iconIndex*4+0x9ac))->SetResource(0,0,(unsigned int)currentIcon);
            }

            FUN_00406d00(generatedPath,260,&UNK_0101996c,&UNK_0101d7fc,
                 (*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_0050d100()->FUN_00408da0());
            FUN_004b7240(generatedPath,resolvedPath,260);
            DAT_011dea10->FUN_004568c0(resolvedPath,&currentIcon,0,0);
            if ((unsigned int)currentIcon != 0) {
                ((UIWidget*)*(void**)((char*)this+iconIndex*4+0xa0c))->SetResource(0,0,(unsigned int)currentIcon);
            }

        } else if ((*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_0050d100()) {
            GO alternativeIcon(0);

            FUN_00406d00(generatedPath,260,&UNK_0101996c,&UNK_0101d7fc,
                 (*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_0050d100()->FUN_00408da0());
            FUN_004b7240(generatedPath,resolvedPath,260);
            DAT_011dea10->FUN_004568c0(resolvedPath,&alternativeIcon,0,0);
            if ((unsigned int)alternativeIcon != 0) {
                ((UIWidget*)*(void**)((char*)this+iconIndex*4+0x9ac))->SetResource(0,0,(unsigned int)alternativeIcon);
            }

            FUN_00406d00(generatedPath,260,&UNK_0101996c,&UNK_0101d7fc,
                 (*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_00503650()->FUN_00408da0());
            FUN_004b7240(generatedPath,resolvedPath,260);
            DAT_011dea10->FUN_004568c0(resolvedPath,&alternativeIcon,0,0);
            if ((unsigned int)alternativeIcon != 0) {
                ((UIWidget*)*(void**)((char*)this+iconIndex*4+0xa0c))->SetResource(0,0,(unsigned int)alternativeIcon);
            }

            FUN_00406d00(generatedPath,260,&UNK_0101996c,&UNK_0101d7fc,
                 (*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_00503650()->FUN_00408da0());
            FUN_004b7240(generatedPath,resolvedPath,260);
            DAT_011dea10->FUN_004568c0(resolvedPath,&alternativeIcon,0,0);
            if ((unsigned int)alternativeIcon != 0) {
                ((UIWidget*)*(void**)((char*)this+iconIndex*4+0x8ec))->SetResource(0,0,(unsigned int)alternativeIcon);
            }

            FUN_00406d00(generatedPath,260,&UNK_0101996c,&UNK_0101d7fc,
                 (*((UIAssetChain*)((char*)this+0xa6c))->FUN_006a7ad0(imageKey))->FUN_0050d100()->FUN_00408da0());
            FUN_004b7240(generatedPath,resolvedPath,260);
            DAT_011dea10->FUN_004568c0(resolvedPath,&alternativeIcon,0,0);
            if ((unsigned int)alternativeIcon != 0) {
                ((UIWidget*)*(void**)((char*)this+iconIndex*4+0x94c))->SetResource(0,0,(unsigned int)alternativeIcon);
            }

        }
    }
}
