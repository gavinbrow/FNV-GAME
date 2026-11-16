struct MessageMenuHandler {
    void FUN_007ab0a0(void* first, void* second, void* third, unsigned int derivedValue);
    void FUN_007aaf80(void* first, void* second, void* third);
};

unsigned int __cdecl FUN_0044a670(void* value);

void MessageMenuHandler::FUN_007aaf80(void* first, void* second, void* third)
{
    FUN_007ab0a0(first, second, third, FUN_0044a670(third));
}