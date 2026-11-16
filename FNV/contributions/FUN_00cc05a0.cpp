// Adapted from unverified 2026-10-25 attempts by two prior contributors.
struct NameReference { unsigned int encoded; int FUN_00cb0a80(); };
struct TextWriter { void** virtualMethods; };
extern "C" const char str_010c9308[];
typedef void (__thiscall* WriteMethod)(TextWriter*, const char*, int);
struct AttributeFormatter {
    int unknown00;
    int unknown04;
    TextWriter* output;
    AttributeFormatter* FUN_00cc05a0(NameReference* name);
};
AttributeFormatter* AttributeFormatter::FUN_00cc05a0(NameReference* name)
{
    if (name->encoded & ~1u) {
        const char* text = (const char*)(name->encoded & ~1u);
        void** methods = output->virtualMethods;
        int length = name->FUN_00cb0a80();
        ((WriteMethod)methods[4])(output, text, length);
    } else {
        TextWriter* writer = output;
        ((WriteMethod)writer->virtualMethods[4])(writer, str_010c9308, 6);
    }
    return this;
}