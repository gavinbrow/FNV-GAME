extern void __cdecl __splitpath_s(
    const char* path,
    char* drive,
    unsigned int driveSize,
    char* directory,
    unsigned int directorySize,
    char* filename,
    unsigned int filenameSize,
    char* extension,
    unsigned int extensionSize);

// @fnv 0x00462d40
void __cdecl FUN_00462d40(
    const char* path,
    char* drive,
    unsigned int driveSize,
    char* directory,
    unsigned int directorySize,
    char* filename,
    unsigned int filenameSize,
    char* extension,
    unsigned int extensionSize)
{
    __splitpath_s(
        path,
        drive,
        driveSize,
        directory,
        directorySize,
        filename,
        filenameSize,
        extension,
        extensionSize);
}
