// @fnv 0x00fda000
extern int DAT_01094d9c;
class FUN_00a0d220_cls { public: void* vtable; void BaseCleanup(); };
namespace fnv_00a00a30
{
    class MapA00 : public FUN_00a0d220_cls {
    public:
        ~MapA00()
        {
            int cleanup_frame[7];
            vtable = &DAT_01094d9c;
            BaseCleanup();
        }
    };
    MapA00 DAT_011f32f4;
}