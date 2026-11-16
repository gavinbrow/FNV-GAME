struct Record20 { int field0,field4,field8,fieldC,field10; };
struct RecordPool {
    Record20* records;
    unsigned short type;
    unsigned short unk06;
    int unk08;
    unsigned short* available;
    int count;
    void __thiscall FUN_00d9bf30(unsigned short typeCode, int first, int second);
    unsigned short __thiscall FUN_00d9c210(int first,int second,const Record20* item);
};
unsigned short RecordPool::FUN_00d9c210(int first,int second,const Record20* item) {
    if (!count) FUN_00d9bf30((unsigned short)(type + 0x80),first,second);
    unsigned short slot=available[count - 1];
    volatile int& remaining = count;
    --remaining;
    records[slot] = *item;
    return slot;
}