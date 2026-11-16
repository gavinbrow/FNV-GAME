struct WatchdogCallback {
    void FUN_00c91620(void** source, int value);
};

struct WatchdogState {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    void* unk10;
    void* unk14;
    WatchdogCallback* callback18;
    void* unk1c;
    void* unk20;
    void* unk24;
    void* unk28;
    void* unk2c;
    void* unk30;
    void* unk34;
    void* unk38;
    void* unk3c;
    void* unk40;
    void* unk44;
    int* value48;
};

void __stdcall FUN_00e48270(WatchdogState* source, int unused)
{
    source->callback18->FUN_00c91620(
        reinterpret_cast<void**>(&source), *source->value48);
}