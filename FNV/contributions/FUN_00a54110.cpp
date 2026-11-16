extern void* __cdecl FUN_00aa1070(unsigned int size);

struct FUN_00a54110 {
    int* pBuffer;
    unsigned int reservedSize;
    unsigned int size;

    FUN_00a54110(unsigned int count);
};

FUN_00a54110::FUN_00a54110(unsigned int count) {
    if (count > 0) {
        pBuffer = static_cast<int*>(FUN_00aa1070(count * sizeof(int)));
    } else {
        pBuffer = 0;
    }
    reservedSize = count;
    size = 0;
}