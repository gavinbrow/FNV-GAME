struct CameraResponse {
    bool __thiscall FUN_00680c30();
};
struct CameraFlag {
    bool __thiscall FUN_008256d0();
};
struct CameraPath : FUN_0058b600_shell {
    bool __thiscall FUN_00440d80();
    CameraResponse* __thiscall FUN_00500940(unsigned int context, unsigned int flags);
    CameraFlag* __thiscall FUN_00891170();
    CameraPath* __thiscall FUN_0058b630(unsigned int index);
    CameraPath* __thiscall FUN_0058b510(unsigned int context, unsigned int flags);
};

CameraPath* CameraPath::FUN_0058b510(unsigned int context, unsigned int flags) {
    CameraPath* result = 0;
    if (!FUN_00440d80()) {
        if (FUN_00500940(context, flags)->FUN_00680c30()) {
            if (reinterpret_cast<FUN_0058b470_shell*>(this)->FUN_0058b470() ||
                !FUN_00891170()->FUN_008256d0()) {
                result = this;
            }
            unsigned int count = FUN_0058b600(this);
            if (count != 0) {
                CameraPath* descendant = 0;
                for (unsigned int i = 0; i < count; ++i) {
                    CameraPath* child = FUN_0058b630(i);
                    if (child != 0)
                        descendant = child->FUN_0058b510(context, flags);
                    if (descendant != 0)
                        break;
                }
                if (descendant != 0)
                    result = descendant;
            }
        }
    }
    return result;
}