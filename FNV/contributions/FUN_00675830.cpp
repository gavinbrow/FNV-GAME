struct PackValue12 { unsigned int first; unsigned int second; unsigned int third; };
struct FUN_00675830_shell : TESPackage {
    int FUN_00672f20(); int FUN_0055b980();
    PackValue12* FUN_00675de0(PackValue12* destination, void* actor);
    PackValue12* FUN_00675360(PackValue12* destination, void* actor);
    PackValue12* FUN_00675830(PackValue12* output, void* actor);
};
PackValue12* FUN_00675830_shell::FUN_00675830(PackValue12* output, void* actor) {
    int packageType = FUN_00672f20();
    PackValue12 successful;
    PackValue12 fallback;
    const PackValue12* sourceValue = packageType == FUN_0055b980() ?
        FUN_00675de0(&successful, actor) : FUN_00675360(&fallback, actor);
    *output = *sourceValue;
    return output;
}