struct Property {
    int value00;
    int value04;
    int value08;
    int value0c;
    void FUN_00ba3840(int count);
};

struct PropertyCollection {
    int field00;
    int field04;
    int field08;
    int field0c;
    int field10;
    int field14;
    int field18;
    int field1c;
    int field20;
    int field24;
    int field28;
    int field2c;
    int field30;
    void FUN_00ba3aa0(int index, Property** entry);
};

struct EffectProperties {
    int field00;
    int field04;
    int field08;
    int field0c;
    int field10;
    int field14;
    int field18;
    int field1c;
    int field20;
    int field24;
    PropertyCollection collection;
    Property first;
    Property second;
    void FUN_00c05370(int unused);
};

void EffectProperties::FUN_00c05370(int) {
    Property* entry = &first;
    entry->FUN_00ba3840(26);
    collection.FUN_00ba3aa0(2, &entry);
    entry = &second;
    entry->FUN_00ba3840(26);
    collection.FUN_00ba3aa0(3, &entry);
}