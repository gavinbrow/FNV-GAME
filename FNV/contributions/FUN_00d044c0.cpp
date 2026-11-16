struct FUNObj
{
    struct Entry
    {
        int first;
        int second;
        int third;
        int fourth;
    };
    Entry entries[15];
    void FUN_00d044c0(int index, int first, int second, int third, int fourth);
};

void FUNObj::FUN_00d044c0(int index, int first, int second, int third, int fourth)
{
    Entry& entry = entries[index + 15];
    entry.first = first;
    entry.second = second;
    entry.third = third;
    entry.fourth = fourth;
}
