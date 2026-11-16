extern int __cdecl _fseek(void* stream, long offset, int origin);
struct FileObject {
    void* unk00;
    void* unk04;
    void* unk08;
    void* stream;
    int unk10;
    bool FUN_00d2bd30(long offset, int origin);
};
bool FileObject::FUN_00d2bd30(long offset, int origin) {
    return _fseek(stream, offset, origin) != 0;
}