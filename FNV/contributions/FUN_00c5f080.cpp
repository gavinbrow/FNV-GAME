class C5F080Node : public C5E7A0Node {
public:
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    C5E7A0Object** items;
    unsigned int count;

    void FUN_00c5f080(C5E7A0Stream& stream);
};

void C5F080Node::FUN_00c5f080(C5E7A0Stream& stream)
{
    unsigned int iterationCount;
    unsigned int initialCount;
    unsigned int countToWrite;
    unsigned int index;

    C5E7A0Node::SaveBinary(stream);

    initialCount = count;
    countToWrite = initialCount;
    C5E7A0SaveUInt(stream, &countToWrite);

    for (index = 0; index < (iterationCount = count); ++index)
        stream.SaveLinkID(items[index]);
}