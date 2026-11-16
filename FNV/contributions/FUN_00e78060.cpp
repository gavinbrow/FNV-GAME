
int __cdecl FUN_00e78060(FUN_00e79f40_Stream* pkInfo)
{
    int totalSize = 0;
    unsigned char* pucSource = (unsigned char*)pkInfo->src;
    unsigned short* pusIndices = pkInfo->indices;
    unsigned char* pucDest = (unsigned char*)pkInfo->dst;

    if (pucSource == 0) {
        unsigned short i = 0;
        if (i < pkInfo->count) {
            do {
                _fnv_zlib_memset(pucDest, 0, pkInfo->elemSize);
                totalSize += pkInfo->elemSize;
                pucDest += pkInfo->dstStride;
                ++i;
            } while (i < pkInfo->count);
        }
        return totalSize;
    }

    unsigned short count = (unsigned short)(pkInfo->type - 16);
    unsigned int nComponents = count > 4 ? 4 : count;

    if (pusIndices) {
        unsigned short i = 0;
        unsigned short index = 0;
        if (i < pkInfo->count) {
            do {
                unsigned char* pRead = pucSource + pusIndices[index] * pkInfo->srcStride;
                ++index;
                unsigned char* pWrite = pucDest;
                unsigned short copied = 0;
                unsigned int remain = 0;
                if ((unsigned short)remain < (unsigned short)nComponents) {
                    remain = (unsigned short)nComponents;
                    copied = (unsigned short)remain;
                    do {
                        *pWrite = *pRead;
                        ++pWrite;
                        pRead += 2;
                    } while (--remain != 0);
                }
                if (copied < 4)
                    _fnv_zlib_memset(pWrite, 0, (unsigned short)(4 - copied));
                totalSize += pkInfo->elemSize;
                pucDest += pkInfo->dstStride;
                ++i;
            } while (i < pkInfo->count);
        }
    } else {
        unsigned short i = 0;
        if (i < pkInfo->count) {
            do {
                unsigned char* pRead = pucSource;
                unsigned char* pWrite = pucDest;
                unsigned short copied = 0;
                unsigned int remain = 0;
                if ((unsigned short)remain < (unsigned short)nComponents) {
                    remain = (unsigned short)nComponents;
                    copied = (unsigned short)remain;
                    do {
                        *pWrite = *pRead;
                        ++pWrite;
                        pRead += 2;
                    } while (--remain != 0);
                }
                if (copied < 4)
                    _fnv_zlib_memset(pWrite, 0, (unsigned short)(4 - copied));
                totalSize += pkInfo->elemSize;
                pucSource += pkInfo->srcStride;
                pucDest += pkInfo->dstStride;
                ++i;
            } while (i < pkInfo->count);
        }
    }
    return totalSize;
}
