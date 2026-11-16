struct FNV_00d61600_Buffer {
    unsigned char* data;
    int length;
    int FUN_00d61600(unsigned char character, int start, int limit);
};
int FNV_00d61600_Buffer::FUN_00d61600(unsigned char character, int start, int limit)
{
    int end = limit;
    int last = length - 1;
    if (end >= last)
        end = last;
    for (int index = start; index < end; ++index) {
        if (data[index] == character)
            return index;
    }
    return -1;
}