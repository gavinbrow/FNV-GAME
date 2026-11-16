
struct FUN_0087a670 {
    unsigned int taskIdentifier;
    unsigned int taskFlags;
    void* taskContext;
    unsigned int taskState;
    FUN_0087a670(unsigned int first, unsigned int second);
};
extern FUN_0087a670* DAT_011df1a8;
void __cdecl FUN_0087b8d0(unsigned int first, unsigned int second)
{
    DAT_011df1a8 = new FUN_0087a670(first, second);
}
