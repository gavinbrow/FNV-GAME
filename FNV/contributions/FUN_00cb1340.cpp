int __cdecl FUN_00cb10d0(const char* text);

bool* __cdecl FUN_00cb1340(bool* result, const char* text, const char* suffix)
{
    int textLength = FUN_00cb10d0(text);
    int suffixLength = FUN_00cb10d0(suffix);
    if (textLength < suffixLength) {
        *result = false;
        return result;
    }
    int offset = textLength - suffixLength;
    for (int i = 0; i < suffixLength; ++i) {
        if (text[offset + i] != suffix[i]) {
            *result = false;
            return result;
        }
    }
    *result = true;
    return result;
}

