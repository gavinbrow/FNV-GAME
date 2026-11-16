struct FUN_00d27ff0_class {int** values; void __thiscall FUN_00d27ff0(int first, int second);};
void FUN_00d27ff0_class::FUN_00d27ff0(int first, int second)
{
    int* data = *values;
    int value = data[first];
    if (first < second) {
        ((volatile int*)data)[first] += data[second];
        (*values)[second] = first;
    } else {
        data[second] += value;
        (*values)[first] = second;
    }
}