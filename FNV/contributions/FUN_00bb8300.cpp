struct FNVArray {
    void* vtable;
    void* elements;
    unsigned short capacity;
    unsigned short count;
    unsigned short elementSize;
    unsigned short growth;

    void Reserve(unsigned int newCapacity);
    void Insert(unsigned int index, char* const* value);

    void Append(char* value) {
        const unsigned int insertionIndex = count;
        if (insertionIndex >= capacity)
            Reserve(insertionIndex + growth);
        Insert(insertionIndex, &value);
    }
};

extern void* gSetting;
extern char* FUN_00a7d550(const char* name, float value);
extern const char gFirstName[];
extern const char gSecondName[];

struct FNVCaller {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28;
    float value2c;
    float value30;
    void Initialize(FNVArray* destination);
    void FUN_00bb8300(FNVArray* destination);
};

void FNVCaller::FUN_00bb8300(FNVArray* destination) {
    Initialize(destination);
    destination->Append(FUN_00a7d330(gSetting));
    destination->Append(FUN_00a7d550(gFirstName, value2c));
    destination->Append(FUN_00a7d550(gSecondName, value30));
}