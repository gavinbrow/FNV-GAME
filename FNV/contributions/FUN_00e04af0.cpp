struct Allocator;
struct BSAudio { int unk00; int unk04; int unk08; int unk0C; Allocator *allocator; };
BSAudio *FUN_00c85750();
struct TypeNode;
struct VisitMap { unsigned int FUN_00cb1930(TypeNode *, int); void FUN_00cb1870(Allocator *, TypeNode *, unsigned int); };
struct Member { void *type; TypeNode *FUN_00d86920(); };
struct TypeNode { TypeNode *FUN_00d46d60(); int FUN_00d46f70(); Member *FUN_00d46f80(int); };
void __cdecl FUN_00e04af0(TypeNode *node, VisitMap *visited, unsigned int mask, void (__cdecl *callback)(Member *)) {
    for (;;) {
        unsigned int flags = visited->FUN_00cb1930(node, 0);
        if (mask & flags)
            return;
        BSAudio *audio = FUN_00c85750();
        visited->FUN_00cb1870(audio->allocator, node, flags | mask);
        for (int i = 0; i < node->FUN_00d46f70(); ++i) {
            Member *member = node->FUN_00d46f80(i);
            TypeNode *child = member->FUN_00d86920();
            if (child)
                FUN_00e04af0(child, visited, mask, callback);
            callback(member);
        }
        if (!node->FUN_00d46d60())
            return;
        node = node->FUN_00d46d60();
    }
}
