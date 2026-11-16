// @fnv 0x00fda210
struct ISetCollection { virtual void dummy0(); virtual void dummy1(); virtual void unregisterSetting(void*); };
extern ISetCollection* DAT_011f96a0;
extern "C" void FUN_0044f570();
struct __declspec(novtable) Setting {void FUN_00404950(); virtual __forceinline ~Setting(){FUN_00404950();}};
struct FUN_0045cf30:Setting {virtual void FUN_0045cf30_virtual(); __forceinline ~FUN_0045cf30(){volatile unsigned int local0; volatile unsigned int local1; volatile unsigned int local2; volatile unsigned int local3; ISetCollection* collection; FUN_0044f570(); collection=DAT_011f96a0; collection->unregisterSetting(this); }};
namespace fnv_00a1aee0 {struct IconSetting {FUN_0045cf30 data; __forceinline ~IconSetting(){}};IconSetting g_011f3368;}
