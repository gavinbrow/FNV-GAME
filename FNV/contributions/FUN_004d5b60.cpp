extern "C" int __cdecl sprintf_s(char* destination, unsigned int size, const char* format, ...);
extern const char DAT_01020d58[];

struct FUN_0040c150 {
    int value0;
    int value4;
    int value8;
    FUN_0040c150(char* text, int index);
};

struct FUN_004d5b60 {
    FUN_0040c150* object;
    int value;
    FUN_004d5b60(int index, int number, int extra);
};

FUN_004d5b60::FUN_004d5b60(int index, int number, int extra) {
    value = extra;
    char* text = new char[13];
    sprintf_s(text, 13, DAT_01020d58, number);
    object = new FUN_0040c150(text, index);
}