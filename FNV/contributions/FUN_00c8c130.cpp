struct RenderArg { unsigned int unknown0,unknown4,unknown8,unknownC; float alpha; };
struct Holder;
struct HolderResult;
struct RenderResult;
struct RenderNode { virtual void method0();
    virtual void method1();
    virtual void method2();
    virtual void method3();
    virtual void method4();
    virtual void method5();
    virtual void method6();
    virtual void method7();
    virtual void method8();
    virtual void method9();
    virtual void method10();
    virtual void method11();
    virtual void method12();
    virtual void method13();
    virtual void method14();
    virtual void method15();
    virtual void method16();
    virtual void method17();
    virtual HolderResult* Fetch(RenderArg*);
    virtual void method19();
    virtual void method20();
    virtual void method21();
    virtual void method22();
    virtual void method23();
    virtual void method24();
    virtual void method25();
    virtual void method26();
    virtual void method27();
    virtual void method28();
    virtual void method29();
    virtual void method30();
    virtual void method31();
    virtual void method32();
    virtual void method33();
    virtual void method34();
    virtual void method35();
    virtual void method36();
    virtual void method37();
    virtual void method38();
    virtual void method39();
    virtual void method40();
    virtual void method41();
    virtual void method42();
    virtual void method43();
    virtual void method44();
    virtual void method45();
    virtual void method46();
    virtual void method47();
    virtual void method48();
    virtual void method49();
    virtual void method50();
    virtual void method51();
    virtual bool NeedsRefresh(RenderArg*); };
struct Holder { unsigned int value00,value04; RenderNode* node08; };
struct HolderResult { unsigned int value00,value04; Holder* link08; };
struct RenderResult {
    unsigned int unknown00;
    Holder *holder04;
    unsigned int unused8;
    unsigned int unused12;
    unsigned int unused16;
    unsigned int unused20;
    unsigned int unused24;
    unsigned int unused28;
    unsigned int unused32;
    unsigned int unused36;
    unsigned int unused40;
    unsigned int unused44;
    unsigned int unused48;
    unsigned int unused52;
    unsigned int unused56;
    unsigned int unused60;
    volatile float colour40; float colour44; volatile float colour48; float colour4C;
};
struct RenderProcessor {
    virtual void method0();
    virtual void method1();
    virtual void method2();
    virtual void method3();
    virtual void method4();
    virtual void method5();
    virtual void method6();
    virtual void method7();
    virtual void method8();
    virtual void method9();
    virtual void method10();
    virtual void method11();
    virtual void method12();
    virtual void method13();
    virtual void method14();
    virtual void method15();
    virtual void method16();
    virtual void method17();
    virtual void method18();
    virtual void method19();
    virtual void method20();
    virtual void method21();
    virtual void method22();
    virtual void method23();
    virtual void method24();
    virtual void method25();
    virtual void method26();
    virtual void method27();
    virtual void method28();
    virtual void method29();
    virtual void method30();
    virtual void method31();
    virtual void method32();
    virtual void method33();
    virtual void method34();
    virtual void method35();
    virtual void method36();
    virtual void method37();
    virtual void method38();
    virtual void method39();
    virtual void method40();
    virtual void method41();
    virtual void method42();
    virtual void method43();
    virtual void method44();
    virtual RenderResult* GetRendered(unsigned char*);
    void FUN_00c84df0(void* input,RenderArg* arg);
    void FUN_00c8c130(void* input,RenderArg* arg);
};
void RenderProcessor::FUN_00c8c130(void* input,RenderArg* arg)
{
    unsigned char ignored;
    RenderResult *result = GetRendered(&ignored);
    RenderNode *node = result->holder04 ? result->holder04->node08 : 0;
    float alpha = arg->alpha;
    if (alpha != 1.0f)
    {
        result->colour40 = result->colour40 * alpha;
        result->colour44 *= alpha;
        result->colour48 *= alpha;
        result->colour4C *= alpha;
    }
    else
    {
        if (node == 0)
            goto complete;
        if (node->NeedsRefresh(arg))
            goto complete;
    }
    {
        HolderResult *replacement = node->Fetch(arg);
        result->holder04 = replacement ? replacement->link08 : 0;
    }
complete:
    FUN_00c84df0(input,arg);
}