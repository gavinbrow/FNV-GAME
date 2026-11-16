struct Quaternion {
    float w, x, y, z;
    Quaternion* FUN_00a2bcf0(Quaternion* out, const Quaternion* right);
};
Quaternion* __cdecl FUN_00a6dc90(Quaternion* out, const Quaternion* in);
void __cdecl FUN_00a88970(Quaternion* out, const Quaternion* in);
extern const double DAT_0109c9e0;

Quaternion* __cdecl FUN_00a6dd50(Quaternion* output, const Quaternion* previous, Quaternion* current, const Quaternion* next) {
    Quaternion inverse;
    inverse.w = current->w;
    inverse.x = -current->x;
    inverse.y = -current->y;
    inverse.z = -current->z;

    Quaternion productNext;
    Quaternion logNext;
    volatile Quaternion* pNext = FUN_00a6dc90(&logNext, inverse.FUN_00a2bcf0(&productNext, next));

    Quaternion productPrev;
    Quaternion logPrev;
    Quaternion* pPrev = FUN_00a6dc90(&logPrev, inverse.FUN_00a2bcf0(&productPrev, previous));

    inverse.w = pNext->w + pPrev->w;
    inverse.x = pNext->x + pPrev->x;
    inverse.y = pNext->y + pPrev->y;
    inverse.z = pNext->z + pPrev->z;

    Quaternion scaled;
    scaled.w = (float)(DAT_0109c9e0 * inverse.w);
    scaled.x = (float)(DAT_0109c9e0 * inverse.x);
    scaled.y = (float)(DAT_0109c9e0 * inverse.y);
    scaled.z = (float)(DAT_0109c9e0 * inverse.z);

    Quaternion exponential;
    FUN_00a88970(&exponential, &scaled);
    current->FUN_00a2bcf0(output, &exponential);
    return output;
}