
struct SlotRecord { int key; };

struct EventToken {
    unsigned int FUN_00982b90();
};

struct EventData {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c;
    EventToken token;
};

struct ChangePacket {
    int sourceKey;
    int eventKind;
    ChangePacket* FUN_004b0680(int key, EventData* event);
};

struct EventRegistry {
    int unk00; int unk04; int unk08; int unk0c;
    unsigned int usedFlags;
    unsigned char unk14;
    unsigned char initialized;
    unsigned int FUN_0044ddc0();
    SlotRecord* FUN_00844160(unsigned int index);
    void FUN_00982f10(EventToken* token);
    void FUN_006db840(ChangePacket* packet);
    bool FUN_00982f40(int key, EventData* event);
};

bool EventRegistry::FUN_00982f40(int key, EventData* event)
{
    for (unsigned int index = 0; index < FUN_0044ddc0(); ++index) {
        SlotRecord* item = FUN_00844160(index);
        if (item->key == key)
            return false;
    }

    if (!initialized)
        FUN_00982f10(&event->token);

    unsigned int flags = event->token.FUN_00982b90();
    if (usedFlags & flags)
        return false;

    usedFlags |= flags;
    {
        ChangePacket packet;
        FUN_006db840(packet.FUN_004b0680(key, event));
    }
    return true;
}
