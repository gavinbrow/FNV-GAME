class PackageLocation;
class TESForm;
struct LocationInputStream {
    void FUN_00865e50(void* destination, unsigned int byteCount, int flags);
    void FUN_00865df0(TESForm* form, int flags);
};
struct FUN_0067fb60_shell : PackageLocation {
    void FUN_0067fb60(LocationInputStream* input);
};
void FUN_0067fb60_shell::FUN_0067fb60(LocationInputStream* input)
{
    input->FUN_00865e50(&eLocType, 1, 0);
    input->FUN_00865e50(&iRad, 4, 0);
    switch (eLocType) {
    case -1:
        break;
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
        input->FUN_00865df0(pObject, 0);
        break;
    case 5:
        input->FUN_00865e50(&pObject, 4, 0);
        break;
    }
}