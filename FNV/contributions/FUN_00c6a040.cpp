struct DispatchState {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int flags;
};

struct DispatchPacket {
    unsigned int status;
    unsigned char mode;
    unsigned int opcode;
    unsigned int selection;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
};

extern DispatchState* __cdecl FUN_00c43490(int object);
extern "C" void __cdecl FUN_00c68900(int object, DispatchPacket* packet, unsigned int dispatcher);
extern "C" unsigned int DAT_011afe94;

unsigned char __cdecl FUN_00c6a040(int object, unsigned char selection,
                                   unsigned char mode, unsigned char overrideCheck)
{
    unsigned char result = 0;
    if (object) {
        if (!overrideCheck) {
            DispatchState* state = FUN_00c43490(object);
            if (!state)
                goto exit;

            unsigned int value = state->flags;
            unsigned int& flags = value;
            if (!(flags &= 2))
                goto exit;
        }

        DispatchPacket packet;
        packet.mode = mode;
        result = 1;
        packet.status = 0;
        packet.opcode = 3;
        packet.selection = selection;

        if (DAT_011afe94)
            FUN_00c68900(object, &packet, DAT_011afe94);
    }
exit:
    return result;
}