struct TileNode; struct TileNodeList { TileNodeList* next; TileNode* parent; TileNode* child; };
struct TileNode { void* virtualTable; TileNodeList* children; float __thiscall FUN_00a011b0(int trait); };
TileNode* __cdecl FUN_00a08fb0(TileNode* root, int target) {
    TileNodeList* cursor;
    {
        TileNode* found;
        {
            if (root && root->FUN_00a011b0(0xFAA) == target) return root;
            TileNodeList* head = root->children;
            cursor = head;
            while (cursor) {
                TileNode** link = &cursor->child;
                cursor = cursor->next;
                found = FUN_00a08fb0(*link, target);
                if (found) return found;
            }
        }
    }
    return 0;
}