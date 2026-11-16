struct ArrowListRemoveHelper {
    void FUN_00905330(ArrowProjectile* const& projectile);
};
struct MiddleHighProcess_00929470 : MiddleHighProcess {
    void FUN_00929470(ArrowProjectile* projectile);
};
void MiddleHighProcess_00929470::FUN_00929470(ArrowProjectile* projectile)
{
    if (!projectile || !pAttachedArrowList)
        return;
    reinterpret_cast<ArrowListRemoveHelper*>(pAttachedArrowList)->FUN_00905330(projectile);
}