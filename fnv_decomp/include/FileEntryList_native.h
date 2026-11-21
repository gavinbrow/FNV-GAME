#ifndef FNV_EXPERIMENT_FILEENTRYLIST_H
#define FNV_EXPERIMENT_FILEENTRYLIST_H
#include "layout_support.h"
class BSFileEntry;
#pragma pack(push, 4)
class FileEntryList
{
  public:
    unsigned char m_ucFileEntryCount, layoutPadding1[3];
    BSFileEntry** m_ppFileEntries;
};
#pragma pack(pop)
FNV_STATIC_ASSERT(sizeof(FileEntryList) == 8);
#endif
