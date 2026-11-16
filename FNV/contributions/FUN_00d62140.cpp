struct SearchBase {
    int FUN_00d61cc0();
};
struct SearchController : SearchBase {
    int FUN_00d61640(int token, int start, int limit);
    int FUN_00d61fc0(int start, int position);
    int FUN_00d62140();
};

int SearchController::FUN_00d62140()
{
    int first = FUN_00d61640(0x2f, 0, 0x7fffffff);
    int second = FUN_00d61640(0x5c, 0, 0x7fffffff);
    if (second <= first)
        second = first;
    if (second >= 0)
        return FUN_00d61fc0(0, second);
    return FUN_00d61cc0();
}
