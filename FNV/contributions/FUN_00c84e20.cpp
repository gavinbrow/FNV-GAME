struct Middle { int unk00; int unk04; unsigned int value; };
struct This
{
    int unk00;
    int unk04;
    Middle* middle;
    void FUN_00c84e20(unsigned int* output);
};
void This::FUN_00c84e20(unsigned int* output)
{
    *output = (this != 0 && middle != 0) ? middle->value : 0;
}
