typedef void (__thiscall *FlushFunction)(void*);
struct BufferWriter
{
    int unknown00;
    int unknown04;
    int capacity;
    int position;
    unsigned char* data;
    void FUN_00e06920(int value);
};
void BufferWriter::FUN_00e06920(int value)
{
    data[capacity - position - 1] = (unsigned char)value;
    ++position;
    if (position >= capacity)
        ((FlushFunction)FUN_00e06490)(this);
    data[capacity - position - 1] = (unsigned char)(value >> 8);
    ++position;
    if (position >= capacity)
        ((FlushFunction)FUN_00e06490)(this);
    data[capacity - position - 1] = (unsigned char)(value >> 16);
    ++position;
    if (position >= capacity)
        ((FlushFunction)FUN_00e06490)(this);
}