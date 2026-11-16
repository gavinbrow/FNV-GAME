extern int DAT_0102f468;
struct FUN_00559eb0
{
    int vtbl;
    int count;
    void* data;
    int flags;
    FUN_00559eb0(int arg);
};
FUN_00559eb0::FUN_00559eb0(int arg)
{
    *(int*)this = (int)&DAT_0102f468;
    *(int*)((char*)this + 4) = arg;
    *(int*)((char*)this + 0x0c) = 0;
    unsigned int byteCount = (unsigned int)(*(int*)((char*)this + 4) << 2);
    *(void**)((char*)this + 8) = NiMalloc(byteCount);
    memset(*(void**)((char*)this + 8), 0, (unsigned int)(*(int*)((char*)this + 4) << 2));
}
