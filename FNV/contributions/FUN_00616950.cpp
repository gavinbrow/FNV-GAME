struct ReputationLimit {
    float* __thiscall FUN_00403e20();
};
extern ReputationLimit DAT_011cba7c;
extern ReputationLimit DAT_011cbc70;
extern ReputationLimit DAT_011cbd68;
struct ReputationTracker {
    float __thiscall FUN_00616a20();
    float __thiscall FUN_00616a40();
    unsigned char __thiscall FUN_00616950(int kind);
};
unsigned char ReputationTracker::FUN_00616950(int kind) {
    float value = 0.0f;
    unsigned char rank = 0;
    if (kind == 1) {
        value = FUN_00616a20();
    } else {
        value = FUN_00616a40();
    }
    if (value >= *DAT_011cba7c.FUN_00403e20() && value < *DAT_011cbc70.FUN_00403e20()) {
        rank = 1;
    } else if (value >= *DAT_011cbc70.FUN_00403e20() && value < *DAT_011cbd68.FUN_00403e20()) {
        rank = 2;
    } else if (value >= *DAT_011cbd68.FUN_00403e20()) {
        rank = 3;
    }
    return rank;
}