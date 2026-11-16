struct IndexedValueTable {
    unsigned int count;
    unsigned int* values;
    unsigned int FUN_004464c0(unsigned int index);
};

unsigned int IndexedValueTable::FUN_004464c0(unsigned int index)
{
    return index < count ? values[index] : 0;
}