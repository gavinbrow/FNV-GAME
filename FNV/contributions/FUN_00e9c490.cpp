struct S_00e9c490_Pt {
    float x, y, z;
    S_00e9c490_Pt FUN_00439ef0(const S_00e9c490_Pt& o) const;
    S_00e9c490_Pt FUN_00439e90(const S_00e9c490_Pt& o) const;
    S_00e9c490_Pt* FUN_0045bb20(S_00e9c490_Pt* out, float s) const;
    float FUN_004b6190(const S_00e9c490_Pt& o) const;
    float FUN_00457990() const;
};
struct S_00e9c490_Entry {
    int unk00;
    int unk04;
    S_00e9c490_Pt unk08;
    float unk14;
};
struct S_00e9c490_Pool {
    int unk00;
    S_00e9c490_Entry* FUN_00e99330(void* node);
};
struct S_00e9c490_Ctx {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    char unk10;
    char unk11;
    short unk12;
    int unk14;
    S_00e9c490_Pool unk18;
};
struct S_00e9c490_Ref {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14;
    int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c;
    unsigned int unk30;
};
struct S_00e9c490_Node {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual S_00e9c490_Ref* v3();
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual int v7();
    int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18;
    int unk1c; int unk20; int unk24; int unk28; int unk2c;
    unsigned int unk30;
    int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48;
    int unk4c; int unk50; int unk54; int unk58; int unk5c; int unk60;
    int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78;
    int unk7c; int unk80; int unk84; int unk88;
    S_00e9c490_Pt unk8c;
};
extern char DAT_0126fa64;
extern char DAT_0126fa65;
extern int DAT_011f4a48;
extern int DAT_011f5f64;
static const float DAT_01011d78 = 0.0f;
bool __cdecl FUN_00eada70(S_00e9c490_Node* node, S_00e9c490_Pt* p1, S_00e9c490_Pt* p2);
bool __cdecl FUN_00e9c6f0(S_00e9c490_Pt* p1, S_00e9c490_Pt* p2, S_00e9c490_Ctx* ctx, S_00e9c490_Node* node);
bool __cdecl FUN_00e9b4f0(S_00e9c490_Pt* p1, S_00e9c490_Pt* p2, S_00e9c490_Ctx* ctx, S_00e9c490_Node* node);
bool __cdecl FUN_0043b300(const void* rtti, S_00e9c490_Node* node);

bool __cdecl FUN_00e9c490(S_00e9c490_Pt* p1, S_00e9c490_Pt* p2, S_00e9c490_Ctx* ctx, S_00e9c490_Node* node)
{
    if (!node)
        return false;
    if (ctx->unk11 && (node->unk30 & 1))
        return false;
    S_00e9c490_Ref* ref = node->v3();
    if (ref && (unsigned char)(ref->unk30 >> 21) & 1)
        return false;
    if (FUN_00eada70(node, p1, p2) || (ref && (unsigned char)(ref->unk30 >> 13) & 1)) {
        if (ref)
            return FUN_00e9c6f0(p1, p2, ctx, node);
        if (node->v7())
            return FUN_00e9b4f0(p1, p2, ctx, node);
        if (DAT_0126fa65 && FUN_0043b300(&DAT_011f4a48, node)) {
            S_00e9c490_Pt d = node->unk8c.FUN_00439ef0(*p1);
            if (p2->FUN_004b6190(d) < DAT_01011d78)
                return false;
            float len = d.FUN_00457990();
            ctx->unk18.FUN_00e99330(node)->unk14 = len;
            return false;
        }
        if (DAT_0126fa64 && FUN_0043b300(&DAT_011f5f64, node)) {
            S_00e9c490_Pt d = node->unk8c.FUN_00439ef0(*p1);
            if (p2->FUN_004b6190(d) < DAT_01011d78)
                return false;
            S_00e9c490_Entry* e = ctx->unk18.FUN_00e99330(node);
            float len = d.FUN_00457990();
            e->unk14 = len;
            if (ctx->unk08 == 1) {
                e->unk08 = p1->FUN_00439e90(*p2->FUN_0045bb20(&d, len));
            }
            return false;
        }
    }
    return false;
}
