#include <string.h>
extern char DAT_010f1844;
void* __cdecl FUN_00aa1070(unsigned int length);
int __cdecl FUN_00a305b0(char* output, unsigned int outputSize, const char* format, const char* value);
struct FnvStringArray {
    unsigned int unk00;
    unsigned int unk04;
    unsigned short capacity;
    unsigned short count;
    unsigned short unk0c;
    unsigned short growth;
    void FUN_0096ad30(unsigned int newCapacity);
    void FUN_0096ae90(unsigned int index, const char** value);
};
struct FnvTextProcessor {
    void FUN_00eab7b0(const char* text, FnvStringArray* array);
};
void FnvTextProcessor::FUN_00eab7b0(const char* text, FnvStringArray* array) {
    unsigned int length = (unsigned int)strlen(text) + 10;
    const char* q = text;
    text = (const char*)FUN_00aa1070(length);
    FUN_00a305b0((char*)text, length, &DAT_010f1844, q);
    unsigned int index = array->count;
    if (index >= array->capacity)
        array->FUN_0096ad30(index + array->growth);
    array->FUN_0096ae90(index, &text);
}
