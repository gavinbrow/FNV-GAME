struct FUN_007fb730_Class {
    float x;
    float y;
    float z;

    FUN_007fb730_Class* __thiscall FUN_007fb730(
        FUN_007fb730_Class* output,
        const FUN_007fb730_Class* input);
};

FUN_007fb730_Class* __thiscall FUN_007fb730_Class::FUN_007fb730(
    FUN_007fb730_Class* output,
    const FUN_007fb730_Class* input)
{
    FUN_007fb730_Class result = *this;

    result.x = result.x + input->x;
    result.y = result.y + input->y;
    result.z = result.z + input->z;

    *output = result;
    return output;
}