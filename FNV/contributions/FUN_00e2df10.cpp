struct ResourceBase { void __thiscall FUN_00cb0c10(); };
struct ResourceHandle { void __thiscall FUN_00e2df10(); };

// @fnv 0x00e2df10
void __thiscall ResourceHandle::FUN_00e2df10()
{
    ResourceBase* base = reinterpret_cast<ResourceBase*>(reinterpret_cast<char*>(this) + 12);
    base->FUN_00cb0c10();
}