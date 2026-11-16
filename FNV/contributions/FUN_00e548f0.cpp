bool* __cdecl FUN_00e548f0(bool* result, int index, float** samples, int endIndex) {
    bool value;
    if (index != endIndex && (*samples)[index] == (*samples)[index + 1]) {
        value = false;
    } else {
        value = true;
    }
    *result = value;
    return result;
}