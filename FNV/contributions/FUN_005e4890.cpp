
class TreeNode;
class NodeList {
public:
    unsigned int FUN_0043b480();
    TreeNode* FUN_0043b4a0(unsigned int index);
};
class KeyName {
public:
    const char* FUN_0043fad0();
};
class TreeNode {
public:
    virtual void unused0();
    virtual void unused1();
    virtual void unused2();
    virtual NodeList* GetChildren();
    virtual void unused4();
    virtual void unused5();
    virtual KeyName* GetKeyName();
};
class FoundResult {
public:
    void FUN_005e4810(unsigned int value, int enabled);
};
extern char DAT_011f49d8[];
FoundResult* __cdecl FUN_00653270(const char*, const char*);
void __cdecl FUN_005e4890(unsigned int key, TreeNode* node) {
    if (node == 0)
        return;
    if (node->GetChildren()) {
        NodeList* children = node->GetChildren();
        for (unsigned int i = 0; i < children->FUN_0043b480(); ++i) {
            FUN_005e4890(key, children->FUN_0043b4a0(i));
        }
    } else if (node->GetKeyName()) {
        KeyName* name = node->GetKeyName();
        const char* text = name->FUN_0043fad0();
        FoundResult* result = FUN_00653270(DAT_011f49d8, text);
        if (result != 0) {
            result->FUN_005e4810(static_cast<unsigned short>(key), 1);
            result->FUN_005e4810(key + 200, 0);
        }
    }
}
