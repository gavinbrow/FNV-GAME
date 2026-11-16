struct CopyRecord {
    unsigned int first;
    unsigned int second;
    unsigned int third;
};
struct IteratorTag {
    unsigned char marker;
};
CopyRecord* __cdecl FUN_00ac2c20(CopyRecord* first, CopyRecord* last, CopyRecord* destination)
{
    CopyRecord* destEnd = destination + (last - first);
    IteratorTag destTag = {};
    IteratorTag sourceTag = {};
    CopyRecord* out;
    CopyRecord* src;
    {
        IteratorTag actualDestTag = destTag;
        IteratorTag actualSourceTag = sourceTag;
        out = destination;
        src = first;
        for (; src != last; ++out, ++src) {
            *out = *src;
        }
    }
    return destEnd;
}