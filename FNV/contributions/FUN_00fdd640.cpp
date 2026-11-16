namespace fnv_00c464c0 { class FUN_00c464c0_child { public: void* FUN_00c46420(int); }; }
extern "C" char DAT_010c1c5c;
extern "C" void* DAT_01202e20;
extern "C" fnv_00c464c0::FUN_00c464c0_child* DAT_01202e24;
struct CleanupFrame
{
    void* result;
    fnv_00c464c0::FUN_00c464c0_child* child;
    void* context;
    fnv_00c464c0::FUN_00c464c0_child* saved;
    fnv_00c464c0::FUN_00c464c0_child* caller;
};
// @fnv 0x00fdd640
void FUN_00fdd640()
{
    CleanupFrame frame;
    DAT_01202e20 = &DAT_010c1c5c;
    frame.child = DAT_01202e24;
    frame.saved = frame.child;
    frame.caller = frame.saved;
    if (frame.caller)
        frame.result = frame.caller->FUN_00c46420(3);
    else
        frame.result = 0;
}
