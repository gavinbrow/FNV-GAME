
struct ResourceBufferOwner {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    unsigned char* buffer10;
    unsigned char* buffer14;
    unsigned char* buffer18;
    unsigned char* buffer1c;
    unsigned char* buffer20;
    unsigned char* buffer24;
    unsigned char* buffer28;
    unsigned char* buffer2c;
    unsigned char* buffer30;
    unsigned char* buffer34;
    unsigned char* buffer38;
    int unk3c;
    unsigned char* buffer40;

    void FUN_00b02d40();
    void FUN_00b274d0();
};

void ResourceBufferOwner::FUN_00b274d0() {
    delete[] buffer10;
    delete[] buffer14;
    delete[] buffer18;
    delete[] buffer24;
    delete[] buffer28;
    delete[] buffer2c;
    delete[] buffer30;
    delete[] buffer1c;
    delete[] buffer20;
    delete[] buffer34;
    delete[] buffer38;

    buffer10 = 0;
    buffer14 = 0;
    buffer18 = 0;
    buffer24 = 0;
    buffer28 = 0;
    buffer2c = 0;
    buffer30 = 0;
    buffer1c = 0;
    buffer20 = 0;
    buffer34 = 0;
    buffer38 = 0;

    delete[] buffer40;
    buffer40 = 0;
    FUN_00b02d40();
}
