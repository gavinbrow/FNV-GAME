struct ProcessingState {
    unsigned int FUN_00aa1810(void* buffer, unsigned int size);
};

void* __cdecl FUN_00aa1070(unsigned int size);
void __cdecl FUN_00ec44d0(void* destination, const void* source, unsigned int size);
void __cdecl FUN_00aa1de0(void* buffer, unsigned int size, void* optionA, void* optionB);
void __cdecl FUN_00aa10f0(void* buffer);

unsigned int __cdecl FUN_00aa1ad0(
    ProcessingState* state,
    const void* data,
    unsigned int size,
    void* optionA,
    void* optionB)
{
    if (size <= 0u)
        return 0;
    void* buffer = FUN_00aa1070(size);
    FUN_00ec44d0(buffer, data, size);
    FUN_00aa1de0(buffer, size, optionA, optionB);
    unsigned int result = state->FUN_00aa1810(buffer, size);
    FUN_00aa10f0(buffer);
    return result;
}