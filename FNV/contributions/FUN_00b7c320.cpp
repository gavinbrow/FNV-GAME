extern unsigned int DAT_011f91e4;
extern int DAT_011ff9dc;
extern int DAT_011ffa18;
void __cdecl FUN_00b97e80(int mode, int unused);
void __cdecl FUN_00b98070(int mode, int unused);
void __cdecl FUN_00b97e30(int mode, int unused);
void __cdecl FUN_00b98380(int mode, int unused);

struct RenderFlagInfo {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int flags18;
};
struct RenderState {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int flags20;
};
struct RenderArguments {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    RenderState* state;
    RenderFlagInfo* info;
};

void __stdcall FUN_00b7c320(RenderArguments* args)
{
    const unsigned int mode = DAT_011f91e4;
    if (mode == 0x250 || mode == 0x251) {
        FUN_00b97e80(3, 0);
    }

    RenderFlagInfo* info = args->info;
    if (info && (info->flags18 & 1u)) {
        FUN_00b98070(0, 0);
    }

    RenderState* state = args->state;
    if ((mode == 6 || mode == 8) && (state->flags20 & 0x40000u) > 0) {
        --DAT_011ff9dc;
        FUN_00b97e30(1, 0);
        --DAT_011ffa18;
        FUN_00b98380(7, 0);
    }
}