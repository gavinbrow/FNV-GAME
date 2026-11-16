struct FNV_00d99f50_Entry { void* value; void* payload; };
struct FNV_00d99f50_Result {
    unsigned char flag;
    FNV_00d99f50_Result() {}
    ~FNV_00d99f50_Result() {}
};
extern "C" void __cdecl FUN_00d98ca0(unsigned char* scratch, const FNV_00d99f50_Entry* entry, void* context, void* left, void* right);
FNV_00d99f50_Result __cdecl FUN_00d99f50(int count, const FNV_00d99f50_Entry* const* entries, void* context, void* left, void* right)
{
    FNV_00d99f50_Result result;
    result.flag = 0;
    for (int i = 0; i < count; ++i) {
        const FNV_00d99f50_Entry* entry = entries[i];
        if (entry && entry->payload) {
            unsigned char temporary;
            FUN_00d98ca0(&temporary, entry, context, left, right);
            unsigned char combined;
            if (result.flag || temporary)
                combined = 1;
            else
                combined = 0;
            result.flag = combined;
        }
    }
    return result;
}