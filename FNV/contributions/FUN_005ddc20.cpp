class GameValue {
public:
    double FUN_00616a60(int component);
};

bool __cdecl func_0x005accb0(
    const void* params, const char* sourceText, void* offset,
    void* reference, void* container, void* script, void* locals,
    GameValue** value, int* component);

bool __cdecl FUN_005ddc20(
    const void* params, const char* sourceText,
    void* reference, void* container, void* script, void* locals,
    double* result, void* offset)
{
    GameValue* value = 0;
    int component;
    if (!func_0x005accb0(params, sourceText, offset,
                         reference, container, script, locals,
                         &value, &component))
        return false;
    if (component >= 0 && component <= 1) {
        *result = value->FUN_00616a60(component);
    } else {
        return false;
    }
    return true;
}