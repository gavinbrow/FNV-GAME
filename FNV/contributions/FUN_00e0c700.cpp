struct Node {
    float value0; float value1; float value2; float value3;
    float value4; float value5; float value6; float value7;
    unsigned short flag0; unsigned short flag1; unsigned short flag2; unsigned short flag3;
    unsigned short flag4; unsigned short flag5; unsigned short flag6; unsigned short flag7;
    Node** children;
    int childCount;
};
void __cdecl FUN_00e0c700(Node* node, int index, float factor) {
    (&node->value0)[index] *= factor;
    (&node->flag0)[index] = 0;
    for (int i = 0; i < node->childCount; ++i)
        FUN_00e0c700(node->children[i], index, factor);
}
