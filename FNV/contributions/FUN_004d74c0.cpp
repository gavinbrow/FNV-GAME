extern char DAT_011c6e10;
void __cdecl FUN_00403d30(void* destination, int pNodeValue, unsigned int size);
typedef int (__stdcall *SendTreeMessage)(void*, int, int, int);

struct FUN_004d74c0_Value {
    int FUN_00453470();
};
struct FUN_004d74c0_Node {
    virtual void f00();
    virtual void f04();
    virtual void f08();
    virtual FUN_004d74c0_Value* getValue();
};
struct FUN_004d74c0_Item {
    unsigned int mask;
    int handle;
    int state;
    int stateMask;
    char* text;
    int textCapacity;
    int image;
    int selectedImage;
    int children;
    FUN_004d74c0_Node* itemData;
    int integral;
    int stateEx;
    void* hwnd;
    int expandedImage;
};

void __cdecl FUN_004d74c0(void* tree, int startingItem, int expandFlags)
{
    FUN_004d74c0_Node* node;
    FUN_004d74c0_Value* pNodeValue;
    FUN_004d74c0_Item item;

    FUN_00403d30(&item, 0, sizeof(item));
    item.mask = 13;
    item.text = &DAT_011c6e10;
    item.textCapacity = 260;

    item.handle = ((SendTreeMessage)DAT_00fdf28c)(tree, 0x110a, 4, startingItem);
    while (item.handle != 0) {
        if (((SendTreeMessage)DAT_00fdf28c)(tree, 0x110c, 0, (int)&item) != 0) {
            node = item.itemData;
            pNodeValue = 0;
            if (node != 0) {
                pNodeValue = node->getValue();
            }
            if (pNodeValue != 0) {
                if (pNodeValue->FUN_00453470() != 0) {
                    ((SendTreeMessage)DAT_00fdf28c)(tree, 0x1102, expandFlags, item.handle);
                    FUN_004d74c0(tree, item.handle, expandFlags);
                }
            }
        }
        item.handle = ((SendTreeMessage)DAT_00fdf28c)(tree, 0x110a, 1, item.handle);
    }
}