
struct GameNode {
    unsigned int unknown00;
    unsigned int unknown04;
    void* payload;

    unsigned short activityFlag() const {
        return *reinterpret_cast<const unsigned short*>(
            reinterpret_cast<const unsigned char*>(this) + 0x204);
    }
};

struct InputRecord {
    void* header;
    void* member04;
    unsigned int member08;
    GameNode* primary;
    GameNode* secondary;
    void* tertiary;

    void* member18() { return reinterpret_cast<unsigned char*>(this) + 0x18; }
    void* member2c() { return reinterpret_cast<unsigned char*>(this) + 0x2c; }
    void* member50() { return reinterpret_cast<unsigned char*>(this) + 0x50; }
};

struct Descriptor {
    int type;
    GameNode* primary;
    GameNode* secondary;
    void* tertiary;
    int control;
    void* data50;
    void* data18;
    unsigned char option0;
    unsigned char option1;
    unsigned char option2;
    void* data04;
    void* output;
    void* data2c;
    int result0;
    int result1;
};

void __cdecl FUN_00d00ca0(void* payload, Descriptor* descriptor);
void __cdecl FUN_00cfff00(GameNode* node, int* index);

void __stdcall FUN_00cfc960(InputRecord* record, void* output, unsigned int unused) {
    Descriptor descriptor;
    descriptor.type = 2;
    descriptor.tertiary = record->tertiary;
    descriptor.secondary = record->secondary;
    descriptor.primary = record->primary;
    descriptor.control = 0;
    descriptor.data50 = record->member50();
    descriptor.data18 = record->member18();
    descriptor.option0 = 0;
    descriptor.option1 = 0;
    descriptor.option2 = 0;
    descriptor.data04 = &record->member04;
    descriptor.output = &output;
    descriptor.data2c = record->member2c();
    descriptor.result0 = 0;
    descriptor.result1 = 0;

    FUN_00d00ca0(record->primary->payload, &descriptor);

    descriptor.type = 0;
    if (record->primary->activityFlag() != 0)
        FUN_00cfff00(record->primary, &descriptor.type);

    descriptor.type = 1;
    if (record->secondary->activityFlag() != 0)
        FUN_00cfff00(record->secondary, &descriptor.type);
}
