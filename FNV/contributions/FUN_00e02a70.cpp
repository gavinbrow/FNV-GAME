struct OffsetView {
    int unk00;
    int unk04;
    char* unk08;
    char* FUN_00e02a70();
};
char* OffsetView::FUN_00e02a70() {
    return unk08 + 12;
}
