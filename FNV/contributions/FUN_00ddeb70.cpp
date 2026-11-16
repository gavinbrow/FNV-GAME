struct Record { float x,y,key; };
struct ComparisonResult
{
    bool value;
    ComparisonResult(bool result) : value(result) {}
    operator bool() const { return value; }
};
__declspec(noinline) ComparisonResult FUN_00ddcda0(const Record& left, const Record& right)
{
    return ComparisonResult(left.key > right.key);
}
inline void SwapRecords(Record& first, Record& second) { __declspec(align(16)) Record temp = second; second = first; first = temp; }
void FUN_00ddeb70(Record* records, int left, int right, int comparator)
{
    int i = left;
    int j = right;
    __declspec(align(16)) Record pivot = records[(left + right) >> 1];
    do
    {
        while (FUN_00ddcda0(records[i], pivot)) ++i;
        while (FUN_00ddcda0(pivot, records[j])) --j;
        if (j >= i)
        {
            if (j != i)
            {
                SwapRecords(records[i], records[j]);
            }
            --j;
            ++i;
        }
    } while (i <= j);
    if (left < j) FUN_00ddeb70(records, left, j, comparator);
    if (i < right) FUN_00ddeb70(records, i, right, comparator);
}




