
struct FNVTreeNode {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    unsigned int taggedName;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    FNVTreeNode** children;
    int childCount;

    FNVTreeNode* __thiscall FUN_00e3ec90(const char* name);
};
FNVTreeNode* __thiscall FNVTreeNode::FUN_00e3ec90(const char* name)
{
    if (name == 0)
        return 0;

    for (int i = 0; i < childCount; ++i) {
        FNVTreeNode* child = children[i];
        if ((child->taggedName & ~1u) != 0) {
            const char* tag = reinterpret_cast<const char*>(child->taggedName & ~1u);
            if (FUN_00cb0fe0(tag, name) == 0)
                return child;
        }

        FNVTreeNode* descendant = child->FUN_00e3ec90(name);
        if (descendant != 0)
            return descendant;
    }
    return 0;
}
