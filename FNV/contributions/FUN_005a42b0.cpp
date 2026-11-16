struct MeasuredValue { unsigned int FUN_005a4320(); };
typedef bool (__thiscall *EligibilityMethod)(void*);
typedef MeasuredValue* (__thiscall *ValueMethod)(void*);
union ExtendedValue { __int64 signedValue; struct { unsigned int low; unsigned int high; }; };
bool __cdecl FUN_005a42b0(void* object, void* unusedContext, void* unusedTarget, double* result)
{
 *result = 0.0;
 if (object && ((EligibilityMethod)(*(void***)object)[64])(object)) {
   void* reference = object;
   MeasuredValue* item = ((ValueMethod)(*(void***)reference)[254])(reference);
   if (item) {
      ExtendedValue count;
      count.low = item->FUN_005a4320();
      count.high = 0;
      *result = static_cast<double>(count.signedValue);
   }
 }
 return true;
}