
struct PacketCallback {
    unsigned int user;
    unsigned char active;
    unsigned int value;
    FUN_0055ebf0* packet;
    unsigned int position;
    unsigned int limit;
    unsigned int state;
};
extern unsigned char UNK_00560870;
unsigned int __cdecl FUN_004a8b00(void*);
void __cdecl FUN_00c68900(void*, PacketCallback*, unsigned char*);
struct FUN_00560350_Class {
    void* FUN_0043fcd0();
    unsigned short FUN_00560350(FUN_0055ebf0* packet);
};

unsigned short FUN_00560350_Class::FUN_00560350(FUN_0055ebf0* packet)
{
    unsigned short result = 0;
    void* object = FUN_0043fcd0();
    if (object != 0) {
        result += 1;
        result += 2;
        FUN_0055ebf0 fallback;
        if (packet == 0)
            packet = &fallback;

        packet->m3 = (unsigned int)this;
        packet->m4 = (unsigned int)object;
        packet->m5 = FUN_004a8b00(object);

        unsigned short total;
        PacketCallback ctx;
        ctx.value = 0x12;
        ctx.active = 1;
        ctx.packet = packet;
        FUN_00c68900(object, &ctx, &UNK_00560870);

        total = packet->m1 + packet->m2;
        if (packet->m1 && packet->m2) {
            packet->m0 |= 4;
            result += total;
        } else if (packet->m1) {
            packet->m0 |= 1;
        }

        if (packet->m1) {
            result += packet->m1 * 0x18;
        }
        unsigned short adjusted = total;
        if (packet->m0 & 2)
            --adjusted;
        result += adjusted * 0x1c;
    }
    return result;
}
