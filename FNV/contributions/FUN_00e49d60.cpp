struct CheckResult {
    unsigned char enabled;
    explicit CheckResult(bool value) : enabled(value) {}
};

struct FilterPredicate {
    virtual void unknownMethod();
    virtual CheckResult evaluate(int first, int second);
};

struct FilterEntry {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    FilterPredicate predicate;
};

struct FilterChain {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    FilterEntry** filters;
    int filterCount;

    CheckResult FUN_00e49d60(int first, int second);
};

CheckResult FilterChain::FUN_00e49d60(int first, int second) {
    for (int index = filterCount - 1; index >= 0; --index) {
        if (!filters[index]->predicate.evaluate(first, second).enabled) {
            return CheckResult(false);
        }
    }
    return CheckResult(true);
}