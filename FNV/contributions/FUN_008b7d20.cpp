struct FactionEntry {
    bool FUN_008b7d00();
    void FUN_005fda50(unsigned int value, bool flag);
};

struct MoreData {
    int unk00;
    int unk04;
    int unk08;
    void* unk0C;
};

struct ExtraData {
    MoreData* FUN_0042e800();
};

struct StatusSubobject {
    void* FUN_005d8a70();
};

struct ActorProxy {
    StatusSubobject* FUN_004181e0();
    ExtraData* FUN_005d43c0();
    unsigned int FUN_008b8ca0(FactionEntry** entries,
                              unsigned int capacity,
                              void* affiliation,
                              void* relatedData);
    void FUN_008b7d20(unsigned int value, bool flag);
};

void ActorProxy::FUN_008b7d20(unsigned int value, bool flag) {
    void* affiliation = reinterpret_cast<StatusSubobject*>(
        reinterpret_cast<char*>(FUN_004181e0()) + 0x30
    )->FUN_005d8a70();

    MoreData* payload = FUN_005d43c0()->FUN_0042e800();

    FactionEntry* factions[128];
    unsigned int numFactions = FUN_008b8ca0(
        factions, 128, affiliation, payload ? payload->unk0C : 0
    );

    for (unsigned int factionIndex = 0; factionIndex < numFactions; ++factionIndex) {
        if (!factions[factionIndex])
            continue;

        if (factions[factionIndex]->FUN_008b7d00())
            factions[factionIndex]->FUN_005fda50(value, flag);
    }
}