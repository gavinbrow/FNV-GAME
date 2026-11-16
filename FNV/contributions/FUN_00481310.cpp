class TESForm;

template <class T>
class NiTMallocInterface;

template <class T, class Allocator>
class NiTLargeArray
{
public:
    unsigned int GetSize();
};

struct RebuildCoordinates
{
    unsigned int formValue;
    unsigned int count;

    void FUN_00462230();
};

class Holder0040e9f0
{
public:
    void WriteToChunk();
};

bool __cdecl FUN_00401500();
void __cdecl AppendChunk(unsigned int chunk, void* data, unsigned int size);

struct ContainerEntry00481310
{
    unsigned int count;
    NiTLargeArray<TESForm*, NiTMallocInterface<TESForm*> >* form;
    Holder0040e9f0* extra;

    void FUN_00481310();
};

// @fnv 0x00481310
void ContainerEntry00481310::FUN_00481310()
{
    RebuildCoordinates record;
    record.count = count;
    record.formValue = form->GetSize();

    if (FUN_00401500())
    {
        record.FUN_00462230();
    }

    // CNTO: the form value and count for one container entry.
    AppendChunk(0x4f544e43u, &record, sizeof(record));

    if (FUN_00401500())
    {
        record.FUN_00462230();
    }

    if (extra != 0)
    {
        extra->WriteToChunk();
    }
}
