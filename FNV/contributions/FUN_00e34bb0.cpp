struct CompressedBlockRange {
    unsigned int alignedStart;
    unsigned int alignedSize;
    unsigned char prefixBytes;
};
class DeltaAnimationStandIn : public hkaDeltaCompressedAnimation {
public:
    void FUN_00e34bb0(unsigned int blockIndex, unsigned int blockCount, CompressedBlockRange* result);
};
void DeltaAnimationStandIn::FUN_00e34bb0(unsigned int blockIndex, unsigned int blockCount, CompressedBlockRange* result)
{
    unsigned int start = m_totalBlockSize * blockIndex +
        (unsigned int)m_dataBuffer.m_data + m_quantizedDataIdx;
    unsigned char offset = (unsigned char)start & 15;
    result->alignedStart = start & ~15u;
    result->prefixBytes = offset;
    unsigned int actualSize = (blockIndex == blockCount - 1) ? m_lastBlockSize : m_totalBlockSize;
    result->alignedSize = (actualSize + offset + 15) & ~15u;
}