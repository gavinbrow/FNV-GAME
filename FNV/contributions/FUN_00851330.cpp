#include <windows.h>
#include "h_f88eb61fd685.h"
class FileEntry {
public:
    unsigned int FUN_007d6950();
    bool FUN_00846ad0();
    bool FUN_00846af0();
    bool FUN_00846b10();
};
int __cdecl FUN_0084fbe0(FileEntry*, FileEntry*);
int __cdecl FUN_00406d50(char*, unsigned int, const char*);
class FileEnumerator {
public:
    BSSimpleList<FileEntry*>* entries;
    unsigned int unk04;
    unsigned int currentIndex;
    void FUN_00851540();
    void FUN_0084ff30(char*);
    void FUN_00851680(const char*, int, bool);
    void FUN_00851330();
};
void FileEnumerator::FUN_00851330()
{
    if (entries) {
        FUN_00851540();
    }
    entries = new BSSimpleList<FileEntry*>;
    currentIndex = 1;

    WIN32_FIND_DATAA findData;
    char szPath[260];
    FUN_0084ff30(szPath);
    FUN_00406d50(szPath, 260, "*");
    FUN_00406d50(szPath, 260, ".fos");

    HANDLE handle = FindFirstFileA(szPath, &findData);
    if (handle == INVALID_HANDLE_VALUE) {
        return;
    }
    do {
        if (findData.nFileSizeLow == 0) {
            continue;
        }
        FUN_00851680(findData.cFileName, -1, false);
    } while (FindNextFileA(handle, &findData));

    FindClose(handle);
    entries->Sort(FUN_0084fbe0);
    FileEntry* first = entries->GetItem();
    if (first && currentIndex <= 1) {
        currentIndex = first->FUN_007d6950();
        if (!first->FUN_00846ad0() &&
            !first->FUN_00846af0() &&
            !first->FUN_00846b10()) {
            ++currentIndex;
        }
    }
}
