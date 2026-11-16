struct RefList;
class RegionAnswer;

struct FUN_004f6f70_cls
{
    virtual void Reserved();
    virtual void* VirtualSlot1();
    unsigned char FUN_004f6f70();
    RegionAnswer* FUN_005f36f0();
};

struct RefList
{
    bool FUN_005f65d0(void** value);
    FUN_004f6f70_cls** FUN_006815c0();
    RefList* FUN_00726070();
};

class RegionAnswer
{
public:
    bool FUN_004f6e60(void* value, bool recursive, bool landTexturesOnly);

    unsigned int unknown;
    RefList entries;
};

// @fnv 0x004f6e60
bool RegionAnswer::FUN_004f6e60(void* value, bool recursive, bool landTexturesOnly)
{
    if (value == 0)
    {
        return false;
    }
    if (entries.FUN_005f65d0(&value))
    {
        return true;
    }
    if (!recursive && !landTexturesOnly)
    {
        return false;
    }

    RefList* node = this != 0 ? &entries : 0;
    while (node != 0 && *node->FUN_006815c0() != 0)
    {
        if (recursive ||
            (landTexturesOnly &&
             (*node->FUN_006815c0())->VirtualSlot1() != 0 &&
             (*node->FUN_006815c0())->FUN_004f6f70()))
        {
            if ((*node->FUN_006815c0())->FUN_005f36f0()->FUN_004f6e60(
                    value, recursive, landTexturesOnly))
            {
                return true;
            }
        }
        node = node->FUN_00726070();
    }
    return false;
}
