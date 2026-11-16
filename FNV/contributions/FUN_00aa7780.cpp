// @fnv 0x00aa7780
struct ReaderShim
{
    int FUN_00aa7780(int* pointer, int unused);
};
int ReaderShim::FUN_00aa7780(int* pointer, int)
{
    int* current = pointer;
    --current;
    return *current;
}