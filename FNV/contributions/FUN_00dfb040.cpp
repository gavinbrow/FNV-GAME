extern float DAT_010dbb3c; extern float DAT_0104da48;
struct ParserContext { int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24,unk28,unk2c,unk30,unk34,unk38,unk3c,unk40,result44; int __thiscall FUN_00e63af0(int, void*,float*); };
struct FloatPair { float first,second; int __thiscall FUN_00e2d0d0(ParserContext*,int,int*,ParserContext**); int __thiscall FUN_00dfb040(ParserContext*,int,int*,ParserContext**); };
int __thiscall FloatPair::FUN_00dfb040(ParserContext* ctx,int input,int* outA,ParserContext** outB)
{
 double initial=DAT_010dbb3c;
 *outB=0; *outA=0;
 first=(float)initial;
 second=DAT_0104da48;
 ctx->result44=ctx->FUN_00e63af0(input,this,&second);
 if(ctx->result44==1)return FUN_00e2d0d0(ctx,input,outA,outB);
 return 2;
}