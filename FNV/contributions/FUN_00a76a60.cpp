struct Item
{
    virtual void Reserved();
    virtual void Destroy();
    volatile long references;
};

struct Owner
{
    unsigned char unk00[0x4c];
    Item* item;
    void FUN_00a76a60(Item* replacement);
};

extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long* value);
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long* value);

void Owner::FUN_00a76a60(Item* replacement)
{
    Item* previous = item;
    if (previous != replacement)
    {
        if (previous && InterlockedDecrement(&previous->references) == 0)
            previous->Destroy();
        item = replacement;
        if (replacement)
            InterlockedIncrement(&replacement->references);
    }
}
