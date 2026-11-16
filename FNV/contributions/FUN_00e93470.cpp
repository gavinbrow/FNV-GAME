#include <string.h>
struct FUN_00e93470_Output {
    unsigned int flags;
    const char* text;
    unsigned int data;
};
struct FUN_00e93470_Class {
    unsigned int m_field00;
    unsigned int m_field04;
    unsigned int m_field08;
    unsigned int m_field0c;
    unsigned char m_copyText;
    void __thiscall FUN_00e93470(FUN_00e93470_Output* out, const char* text, unsigned int data);
};
extern "C" void* __cdecl FUN_00aa1070(unsigned int length);
extern "C" void __cdecl FUN_00ec65a6(void* destination, unsigned int length, const char* source);

void FUN_00e93470_Class::FUN_00e93470(FUN_00e93470_Output* out, const char* text, unsigned int data)
{
    if (m_copyText) {
        const unsigned int length = (unsigned int)strlen(text) + 1;
        void* copied = FUN_00aa1070(length);
        out->text = static_cast<const char*>(copied);
        FUN_00ec65a6(copied, length, text);
    } else {
        out->text = text;
    }
    out->data = data;
}
