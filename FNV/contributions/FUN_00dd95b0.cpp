struct FUN_00dd95b0_Source { virtual void unused0(); virtual void unused1(); virtual int GetBytes(const char** bytes, int* count); };
struct FUN_00cb18f0_t { int unk00; int unk04; int FUN_00cb1fb0(int value); };
struct FUN_00dd95b0_Outer {
    int unk00; int unk04; FUN_00cb18f0_t output;
    void FUN_00dd95b0(FUN_00dd95b0_Source* source);
};
void FUN_00dd95b0_Outer::FUN_00dd95b0(FUN_00dd95b0_Source* source) {
    int count;
    const char* bytes;
    bytes = 0;
    count = 0;
    source->GetBytes(&bytes, &count);
    for (int i = 0; i < count; ++i)
        output.FUN_00cb1fb0((unsigned char)bytes[i]);
}
