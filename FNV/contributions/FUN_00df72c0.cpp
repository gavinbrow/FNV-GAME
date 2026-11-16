struct Data {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    volatile Data *value;
};
struct TargetBase { void FUN_00df7230(volatile Data *value); };
struct FUN_00df72c0_class {
    int unk00;
    int unk04;
    void FUN_00df72c0(volatile Data *value);
};
void FUN_00df72c0_class::FUN_00df72c0(volatile Data *value) {
    value = value->value;
    char *p = (char *)this;
    p -= 8;
    ((TargetBase *)p)->FUN_00df7230(value);
}


