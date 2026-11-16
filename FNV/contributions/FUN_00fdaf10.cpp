// @fnv 0x00fdaf10
typedef long (__stdcall *InterlockedDecrementFn)(volatile long*);
extern InterlockedDecrementFn DAT_00fdf1c4;
struct RefObject
{
    virtual ~RefObject();
    virtual void DeleteThis();
    volatile long count;
};
extern RefObject* DAT_011f453c[10];
void FUN_00fdaf10()
{
    InterlockedDecrementFn decrement = DAT_00fdf1c4;
    RefObject** current = DAT_011f453c;
    int remaining = 9;
    do
    {
        RefObject* object = *--current;
        if (object && decrement(&object->count) == 0)
        {
            object->DeleteThis();
        }
    } while (--remaining >= 0);
}
