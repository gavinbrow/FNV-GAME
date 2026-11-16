#include <windows.h>
struct FUN_00d605d0_Class { void FUN_00d605d0(unsigned int); };
struct FUN_00d60940_Class { void FUN_00d60940(unsigned int); };
struct Stream : FUN_00d605d0_Class { void FUN_00d60960(unsigned int); void FUN_00d609a0(unsigned int,int); char* FUN_00d607e0(void*); };
struct Output { int state; Stream* stream; CRITICAL_SECTION* lock; int FUN_00dd9830(unsigned int,unsigned int,unsigned int); };
int Output::FUN_00dd9830(unsigned int first,unsigned int second,unsigned int third) {
 EnterCriticalSection(lock);
 if(stream) {
  stream->FUN_00d60960(17);
  stream->FUN_00d605d0(3);
  stream->FUN_00d60960(first);
  stream->FUN_00d609a0(second,0);
  ((FUN_00d60940_Class*)stream)->FUN_00d60940(third);
 }
 bool failed=stream && *stream->FUN_00d607e0(&first);
 LeaveCriticalSection(lock);
 return !failed;
}
