struct FUN_00e05370_Entry { int id; void* key; };
struct FUN_00e05370_Callback { int unknown0; int unknown4; void (__cdecl* invoke)(int); };
struct FUN_00e05370_List { FUN_00e05370_Entry* data; int capacity; int lastIndex; void FUN_00cb1a60(); };
struct FUN_00e05370_Map { int unknown0; int count; int unknown8; int unknownC; int unknown10; void* table; FUN_00e05370_Callback* FUN_00d87800(void* key, int defaultValue); void FUN_00d87760(); };
struct FUN_00e05370_Class { int unknown0; int unknown4; int field08; int unknownC; FUN_00e05370_List list; FUN_00e05370_Map map; void FUN_00e05370(); };
void FUN_00e05370_Class::FUN_00e05370()
{
    if (map.table && map.count > 0) {
        int limit = list.lastIndex;
        int index = 0;
        while (index <= limit && list.data[index].id == -1)
            ++index;
        if (index <= list.lastIndex) {
            do {
                void* key = list.data[index].key;
                FUN_00e05370_Callback* cb = map.FUN_00d87800(key, 0);
                if (cb && cb->invoke)
                    cb->invoke(list.data[index].id);
                int next = index + 1;
                while (next <= list.lastIndex && list.data[next].id == -1)
                    ++next;
                index = next;
            } while (index <= list.lastIndex);
        }
    }
    field08 = 0;
    list.FUN_00cb1a60();
    map.FUN_00d87760();
}