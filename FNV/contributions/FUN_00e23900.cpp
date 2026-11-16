
struct SearchItem { int unk00; int unk04; unsigned int hashX; unsigned int hashY; };
struct SearchPath { SearchItem** nodes; int depth; };
struct HashEntry { SearchItem* left; SearchItem* right; int result; };
struct HashBucket { HashEntry* entries; int count; int unk08; };
struct HashTable { HashBucket* buckets; unsigned int bucketCount; };
struct SearchOwner { int FUN_00e23900(SearchPath* path); };
int SearchOwner::FUN_00e23900(SearchPath* path)
{
    SearchItem** nodes = path->nodes;
    HashTable* table;
    if (nodes == 0 || (table = *(HashTable**)((char*)this + 0x24c)) == 0)
        return 0;
    int depth = path->depth;
    SearchItem* left = nodes[depth + 2];
    SearchItem* right = nodes[((9 >> (depth * 2)) & 3) + 2];
    unsigned int leftHash = left->hashY * 0x3442a5u;
    leftHash += left->hashX * 0x21528000u;
    unsigned int rightHash = right->hashY * 0x1958e9u;
    rightHash -= right->hashX * 0x538b8000u;
    HashBucket* bucket = table->buckets + ((leftHash ^ rightHash) % table->bucketCount);
    int count = bucket->count;
    int i = 0;
    if (count > 0) {
        HashEntry* entries = bucket->entries;
        HashEntry* cursor = entries;
        do {
            if (cursor->left == left && cursor->right == right) {
                if (i == -1)
                    return 0;
                HashEntry* found = entries + i;
                if (found == 0)
                    return 0;
                return found->result;
            }
            ++i;
            ++cursor;
        } while (i < count);
    }
    return 0;
}
