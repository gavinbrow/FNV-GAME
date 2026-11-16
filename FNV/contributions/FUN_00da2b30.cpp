struct CallbackHolder {
    int unk00;
    int unk04;
    int unk08;
    void (__stdcall *callback)(void* argument);
};

extern void* (__stdcall *DAT_00fdf110)();

struct FUN_00da2b30_Class {
    int unk00;
    int unk04;
    CallbackHolder* holder;

    void FUN_00da2b30();
};

void FUN_00da2b30_Class::FUN_00da2b30()
{
    CallbackHolder* value = holder;
    if (value->callback) {
        value->callback(DAT_00fdf110());
    }
}
