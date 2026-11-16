
int __cdecl FUN_00404dc0(const char* lhs, const char* rhs);

struct FUN_00489f20_shell : TESModelList {
    bool FUN_00489f20(const char* filename);
};

bool FUN_00489f20_shell::FUN_00489f20(const char* filename)
{
    if (nifFilenames.IsEmpty() || filename == 0)
        return false;

    BSSimpleList<const char*>* entry = &nifFilenames;
    while (entry != 0) {
        const char* value = entry->GetItem();
        if (value && FUN_00404dc0(value, filename) == 0)
            return true;
        entry = entry->GetNext();
    }

    return false;
}