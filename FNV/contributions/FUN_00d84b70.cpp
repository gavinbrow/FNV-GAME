struct ValidationResult {
    unsigned char value;
    ValidationResult(bool result) : value(result) {}
};
struct Transform { ValidationResult isOrthonormal(float tolerance); };
struct FUN_00d84b70 { ValidationResult CheckValid(); };
ValidationResult FUN_00d84b70::CheckValid()
{
    Transform* first = (Transform*)((char*)this + 0x20);
    Transform* second = (Transform*)((char*)this + 0x60);
    return first->isOrthonormal(0.001f).value &&
           second->isOrthonormal(0.001f).value;
}
