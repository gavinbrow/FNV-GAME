// The target allocates 0x14 bytes.  These five unknown fields
// preserve the object layout until the constructor's fields are identified.
struct RuntimeWorkItem : FUN_0055a220 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
};

struct RuntimeWorkItemFactory {
    RuntimeWorkItem* FUN_0055a160();
};

RuntimeWorkItem* RuntimeWorkItemFactory::FUN_0055a160()
{
    return new RuntimeWorkItem;
}