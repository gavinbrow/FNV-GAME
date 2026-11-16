struct TreeEval {
    TreeEval() { FUN_00b029f0(); }
    ~TreeEval() { FUN_00b02ac0(); }
    void FUN_00b029f0();
    void FUN_00b02ac0();
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    float leafScale;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned char leftEnabled, leftU79, leftU7a, leftU7b;
    float leftAlpha;
    int leftLevel;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8c;
    unsigned int unk90;
    unsigned int unk94;
    unsigned int unk98;
    unsigned int unk9c;
    unsigned int unka0;
    unsigned int unka4;
    unsigned int unka8;
    unsigned int unkac;
    unsigned int unkb0;
    unsigned char rightEnabled, rightUb5, rightUb6, rightUb7;
    float rightAlpha;
    int rightLevel;
    unsigned int unkc0;
    unsigned int unkc4;
    unsigned int unkc8;
    unsigned int unkcc;
    unsigned int unkd0;
    unsigned int unkd4;
    unsigned int unkd8;
    unsigned int unkdc;
    unsigned int unke0;
    unsigned int unke4;
    unsigned int unke8;
    unsigned int unkec;
    unsigned char opacityEnabled, opacityF1, opacityF2, opacityF3;
    unsigned int unkf4;
    unsigned int unkf8;
    float opacity;
    unsigned int unk100;
    unsigned int unk104;
    unsigned int unk108;
    unsigned int unk10c;
    unsigned int unk110;
    unsigned int unk114;
    unsigned int unk118;
    unsigned int unk11c;
    unsigned int unk120;
    unsigned int unk124;
    unsigned int unk128;
    unsigned int unk12c;
};
struct RuntimeOps {
    void FUN_00b065e0(float, float, float);
    void FUN_00b08480(float);
    void FUN_00b08200();
    float FUN_00b08440();
    short FUN_00b08530(float);
    void FUN_00b0ad00(TreeEval*, float);
    RuntimeOps* FUN_00b051e0();
    RuntimeOps* FUN_00b08af0(void*);
};
struct SceneNode {
    void FUN_00bb39e0(void*,void*);
};
struct NodeHandle {
    SceneNode* FUN_00559450();
};
struct TreeCallback {
    virtual void v00();
    virtual void v01();
    virtual void v02();
    virtual void v03();
    virtual void v04();
    virtual void v05();
    virtual void v06();
    virtual void v07();
    virtual void v08();
    virtual void v09();
    virtual void v0a();
    virtual void v0b();
    virtual void v0c();
    virtual void v0d();
    virtual void v0e();
    virtual void v0f();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual void v13();
    virtual void v14();
    virtual void v15();
    virtual void v16();
    virtual void v17();
    virtual void v18();
    virtual void v19();
    virtual void v1a();
    virtual void v1b();
    virtual void v1c();
    virtual void v1d();
    virtual void v1e();
    virtual void v1f();
    virtual void v20();
    virtual void v21();
    virtual void v22();
    virtual void v23();
    virtual void v24();
    virtual void v25();
    virtual void v26();
    virtual void v27();
    virtual void v28();
    virtual void v29();
    virtual void v2a();
    virtual void v2b();
    virtual void v2c();
    virtual void v2d();
    virtual void v2e();
    virtual void v2f();
    virtual void v30();
    virtual void v31();
    virtual void v32();
    virtual void v33();
    virtual void v34();
    virtual void v35();
    virtual void v36();
    virtual void v37();
    virtual void v38();
    virtual void v39();
    virtual void v3a();
    virtual void v3b();
    virtual void v3c();
    virtual void v3d();
    virtual void v3e();
    virtual void v3f();
    virtual int IsReady();
    virtual void v41();
    virtual void v42();
    virtual void v43();
    virtual void v44();
    virtual void v45();
    virtual void v46();
    virtual void v47();
    virtual void v48();
    virtual void v49();
    virtual void SetLeafEnabled(unsigned char);
    virtual void SetBranchEnabled(unsigned char);
    virtual void SetTopEnabled(unsigned char);
    virtual void SetLeafLod(unsigned short, unsigned char);
    virtual void SetBranchLod(unsigned short, unsigned char);
    virtual void SetTopAlpha(unsigned char);
    Point3X* FUN_0045bb80();
};
unsigned char __cdecl FUN_0054ee20();
unsigned char __cdecl FUN_005b9790();
struct TreeActor {
    int unk00,unk04,unk08;
    RuntimeOps* runtime;
    int unk10,unk14,unk18,unk1c;
    NodeHandle handle;
    short FUN_00669990();
    short FUN_006699d0();
    void FUN_00669a10(TreeCallback*);
};
void TreeActor::FUN_00669a10(TreeCallback* receiver)
{
    TreeEval info;
    float fade;
    unsigned char visible;
    short leaf;
    {
        Point3X worldPos;
        void* pNode = 0;
        short levelCount;
    if (!receiver || !receiver->IsReady())
        return;
    if (!runtime)
        return;
    if (!FUN_0054ee20())
        return;
    worldPos = *receiver->FUN_0045bb80();
    runtime->FUN_00b065e0(worldPos.x,worldPos.y,worldPos.z);

    if (FUN_00669fb0()) {
        runtime->FUN_00b08480(1.0f);
        fade = 1.0f;
    } else {
        runtime->FUN_00b08200();
        fade = runtime->FUN_00b08440();
    }
    runtime->FUN_00b0ad00(&info,fade);
    visible = 0;
    if (info.opacityEnabled) {
        visible = 1;
        receiver->SetTopAlpha((unsigned char)info.opacity);
    }
    receiver->SetTopEnabled(visible);
    if (fade <= 0.0f) {
        receiver->SetLeafEnabled(0);
        receiver->SetBranchEnabled(0);
        return;
    }
    visible = 0;
    levelCount = FUN_00669990();
    if (levelCount > 0) {
        short preferred = runtime->FUN_00b08530(runtime->FUN_00b08440());
        for(leaf=0; leaf<levelCount; ++leaf) {
            if (preferred==leaf) {
                visible=1;
                receiver->SetLeafLod(leaf,(unsigned char)info.leafScale);
            } else {
                receiver->SetLeafLod(leaf,255);
            }
        }
    }
    receiver->SetLeafEnabled(visible);
    if (!FUN_005b9790()) {
        receiver->SetBranchEnabled(0);
        return;
    }
    visible=0;
    levelCount=FUN_006699d0();
    if (levelCount>0) {
        if (info.leftEnabled || info.rightEnabled) {
            for(leaf=0;leaf<levelCount;++leaf) {
                if(info.leftEnabled && info.leftLevel==leaf) {
                    visible=1;
                    receiver->SetBranchLod(leaf,(unsigned char)info.leftAlpha);
                } else if(info.rightEnabled && info.rightLevel==leaf) {
                    visible=1;
                    receiver->SetBranchLod(leaf,(unsigned char)info.rightAlpha);
                } else {
                    receiver->SetBranchLod(leaf,255);
                }
            }
        }
        if(handle.FUN_00559450()) {
            void* lightPtr = runtime->FUN_00b051e0()
                ? runtime->FUN_00b051e0()->FUN_00b08af0(&pNode)
                : runtime->FUN_00b08af0(&pNode);
            handle.FUN_00559450()->FUN_00bb39e0(lightPtr,pNode);
        }
    }
    receiver->SetBranchEnabled(visible);
    }
}
