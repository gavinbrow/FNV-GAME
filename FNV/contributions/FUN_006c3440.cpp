struct Vector3 {
    float x;
    float y;
    float z;
};

struct RotationMatrix {
    void FUN_00439ef0(Vector3* result, const Vector3* input);
};

struct WorldObject;

struct Reference {
    WorldObject* FUN_00559450();
};

extern float g_0106c3a4;
extern float g_0106c3a8;

void __cdecl FUN_006c3440(Reference* reference)
{
    Vector3 transformed;
    reinterpret_cast<RotationMatrix*>(
        reinterpret_cast<char*>(reference->FUN_00559450()) + 0x64
    )->FUN_00439ef0(
        &transformed,
        reinterpret_cast<const Vector3*>(
            reinterpret_cast<char*>(reference->FUN_00559450()) + 0x58
        )
    );

    if (transformed.z < g_0106c3a4) {
        *reinterpret_cast<unsigned char*>(
            reinterpret_cast<char*>(reference->FUN_00559450()) + 0x74
        ) = 0;
    } else {
        float zLimit = g_0106c3a4 * 2.0;
        if (zLimit > transformed.z &&
            transformed.x < g_0106c3a8 &&
            transformed.y < g_0106c3a8) {
            *reinterpret_cast<unsigned char*>(
                reinterpret_cast<char*>(reference->FUN_00559450()) + 0x74
            ) = 0;
        } else {
            *reinterpret_cast<unsigned char*>(
                reinterpret_cast<char*>(reference->FUN_00559450()) + 0x74
            ) = 1;
        }
    }
}