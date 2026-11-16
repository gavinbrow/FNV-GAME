class TESSound
{
public:
    int Deallocate();
};

struct FUN_0040a1e0_shell : MagicItem
{
    int FUN_0040a1e0();
};

int FUN_0040a1e0_shell::FUN_0040a1e0()
{
    MagicItemForm* form = dynamic_cast<MagicItemForm*>(static_cast<MagicItem*>(this));
    MagicItemObject* object = dynamic_cast<MagicItemObject*>(static_cast<MagicItem*>(this));
    if (form != 0)
        return reinterpret_cast<TESSound*>(form)->Deallocate();
    else if (object != 0)
        return reinterpret_cast<TESSound*>(object)->Deallocate();
    return 0;
}