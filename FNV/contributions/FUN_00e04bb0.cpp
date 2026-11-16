struct Allocator;
struct BSAudio { int unk00,unk04,unk08,unk0C; Allocator* allocator; };
BSAudio* FUN_00c85750();
struct TypeNode;
struct VisitMap { unsigned int FUN_00cb1930(TypeNode*, int); void FUN_00cb1870(Allocator*, TypeNode*, unsigned int); };
struct Member { int unk00; void* type; TypeNode* FUN_00d86910(); };
struct TypeNode { TypeNode* FUN_00d46d60(); int FUN_00d46f70(); Member* FUN_00d46f80(int); };
struct Property { int unk00,unk04,unk08,unk0C; short unk10; unsigned short offset; };
struct Registry { Property* FUN_00d46fe0(const char*); };
extern Registry DAT_0126ed90;
extern char DAT_010ea4cc[], DAT_010e5210[];
void FUN_00e04bb0(TypeNode* node, VisitMap* visited)
{
    unsigned int flags = visited->FUN_00cb1930(node, 0);
    if (!(flags & 1))
    {
        BSAudio* audio = FUN_00c85750();
        visited->FUN_00cb1870(audio->allocator, node, flags | 1);
        unsigned int offset = DAT_0126ed90.FUN_00d46fe0(DAT_010ea4cc)->offset;
        TypeNode* ancestor = node;
        while (ancestor->FUN_00d46d60())
        {
            *reinterpret_cast<int*>(reinterpret_cast<char*>(ancestor) + offset) = 0;
            ancestor = ancestor->FUN_00d46d60();
        }
        if (*reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(ancestor) + offset))
        {
            unsigned int countOffset = DAT_0126ed90.FUN_00d46fe0(DAT_010e5210)->offset;
            ++*reinterpret_cast<int*>(reinterpret_cast<char*>(ancestor) + countOffset);
        }
        *reinterpret_cast<int*>(reinterpret_cast<char*>(ancestor) + offset) = 0;
        for (int i = 0; i < node->FUN_00d46f70(); ++i)
        {
            Member* member = node->FUN_00d46f80(i);
            if (member->type)
                FUN_00e04bb0(member->FUN_00d86910(), visited);
        }
        if (node->FUN_00d46d60())
            FUN_00e04bb0(node->FUN_00d46d60(), visited);
    }
}

