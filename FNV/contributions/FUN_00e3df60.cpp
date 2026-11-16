struct ScriptRecord {
    unsigned int identifier;
    unsigned short flags;
    short type;
    unsigned int value;
};

struct ScriptRecordList {
    ScriptRecord* records;
    int count;

    ScriptRecord* FUN_00e3df60(int type, int occurrence);
};

ScriptRecord* ScriptRecordList::FUN_00e3df60(int type, int occurrence)
{
    int matched = 0;
    for (int index = 0; index < count; ++index) {
        if (records[index].type == static_cast<short>(type)) {
            if (matched == occurrence) {
                return &records[index];
            }
            ++matched;
        }
    }
    return 0;
}