struct FUN_00680830_shell : PackageTarget {
    void FUN_00680830(void* unused);
};

void FUN_00680830_shell::FUN_00680830(void* unused)
{
    switch (eTargType) {
    case PACK_TARG_TYPE_PTT_REFERENCE:
    case PACK_TARG_TYPE_PTT_OBJECT:
        pRefOrObj = pRefOrObj
            ? TESForm::GetFormByNumericID((unsigned int)pRefOrObj)
            : 0;
        break;
    }
}
