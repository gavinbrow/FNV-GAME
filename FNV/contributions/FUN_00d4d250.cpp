struct CollisionTarget {
    int unknown00;
    int unknown04;
    int unknown08;
    int unknown0c;
    int unknown10;
    unsigned int collisionKey;
};
struct CollisionEntry { int shapeKey; CollisionTarget* target; };
void __cdecl FUN_00d4d250(CollisionEntry* entries, int left, int right, int context)
{
    int i = left;
    int j = right;
    __declspec(align(16)) CollisionEntry pivot = entries[(i + j) >> 1];
    do {
        while (entries[i].target->collisionKey < pivot.target->collisionKey) ++i;
        while (pivot.target->collisionKey < entries[j].target->collisionKey) --j;
        if (j < i) break;
        if (j != i) {
            CollisionEntry temp = entries[j];
            entries[j] = entries[i];
            entries[i] = temp;
        }
        --j;
        ++i;
    } while (i <= j);
    if (left < j) FUN_00d4d250(entries, left, j, context);
    if (i < right) FUN_00d4d250(entries, i, right, context);
}
