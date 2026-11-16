struct RcObject {
    void FUN_00c90510();
    void FUN_00c905b0();
};
struct SortEntry {
    RcObject* object;
    int key;
    int value;
};
void __cdecl FUN_00e3eec0(SortEntry* entries, int index, int count, int compare);
void __cdecl FUN_00e3eff0(SortEntry* entries, int count, int compare)
{
    int remaining = count;
    int index = count / 2;
    while (index > 0) {
        FUN_00e3eec0(entries, index, count, compare);
        --index;
    }
    if (remaining >= 1) {
        SortEntry* last = &entries[remaining - 1];
        do {
            if (entries->object)
                entries->object->FUN_00c90510();
            SortEntry copy = *entries;
            if (entries != last) {
                RcObject* newObject = last->object;
                if (newObject)
                    newObject->FUN_00c90510();
                if (entries->object)
                    entries->object->FUN_00c905b0();
                entries->object = newObject;
            }
            entries->key = last->key;
            entries->value = last->value;
            if (last != &copy) {
                if (copy.object)
                    copy.object->FUN_00c90510();
                if (last->object)
                    last->object->FUN_00c905b0();
                last->object = copy.object;
            }
            last->key = copy.key;
            last->value = copy.value;
            --remaining;
            --last;
            FUN_00e3eec0(entries, 1, remaining, compare);
            if (copy.object)
                copy.object->FUN_00c905b0();
        } while (remaining >= 1);
    }
}