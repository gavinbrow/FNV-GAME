
struct TimeInput { float __thiscall FUN_00527a40(FUN_00985bb0_Class* owner); };
extern float _DAT_0108d5a0;
extern double _DAT_0108d598;
extern double _DAT_01020758;
float __cdecl FUN_0040ebd0(float value, float limit);

struct CombatClock : FUN_00985bb0_Class
{
    float __thiscall FUN_00985b40(TimeInput* timeInput);
};
float CombatClock::FUN_00985b40(TimeInput* timeInput)
{
    float elapsed;
    {
        float current = FUN_00985bb0();
        elapsed = timeInput->FUN_00527a40(this);
        elapsed = FUN_0040ebd0(elapsed, _DAT_0108d5a0);
        current -= elapsed / _DAT_0108d598;
        if (*reinterpret_cast<int*>(&_ts._pad[4]) != 0)
            current += _DAT_01020758;
        return current;
    }
}
