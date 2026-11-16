
struct Vector3Words {
    unsigned int x;
    unsigned int y;
    unsigned int z;
};
struct FUN_00b71b40_shell {
    Vector3Words FUN_00b71b40() const;
};
Vector3Words FUN_00b71b40_shell::FUN_00b71b40() const
{
    const Vector3Words& position = *reinterpret_cast<const Vector3Words*>(
        reinterpret_cast<const unsigned char*>(this) + 0x1e4);
    return position;
}
