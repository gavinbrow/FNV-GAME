unsigned int __cdecl FUN_00ec7c56();
void __cdecl FUN_00ec7c66(void* dst, unsigned int dstSize, const void* src, unsigned int count);

struct FUN_00ad4040_Class {
    char* __thiscall FUN_00ad4040(char* src, char* srcEnd, char* dst, unsigned int dstSize);
};

char* __thiscall FUN_00ad4040_Class::FUN_00ad4040(char* src, char* srcEnd, char* dst, unsigned int dstSize)
{
    if (dstSize < (unsigned int)(srcEnd - src)) {
        FUN_00ec7c56();
    }
    FUN_00ec7c66(dst, dstSize, src, srcEnd - src);
    return srcEnd;
}
