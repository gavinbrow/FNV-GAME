#include "h_40a74db9745f.h"

struct FUN_0063bb70_value {
    int value;
};

struct FUN_0063bb70_result {
    int value0;
    int value1;
    int value2;
    int value3;
};

struct FUN_0063bb70_shell {
    void FUN_0063bb70(
        FUN_0063bb70_result* result,
        FUN_0063bc60_shell* first,
        FUN_0063bc60_shell* second,
        int value,
        FUN_0063bb70_value* source1,
        FUN_0063bb70_value* source2);
};

void FUN_0063bb70_shell::FUN_0063bb70(
    FUN_0063bb70_result* result,
    FUN_0063bc60_shell* first,
    FUN_0063bc60_shell* second,
    int value,
    FUN_0063bb70_value* source1,
    FUN_0063bb70_value* source2)
{
    if (first == 0)
        return;

    result->value0 = first->FUN_0063bc60(value, source1->value);
    result->value1 = first->FUN_0063bc60(value, source2->value);

    if (second != 0) {
        result->value2 = second->FUN_0063bc60(value, source1->value);
        result->value3 = second->FUN_0063bc60(value, source2->value);

        if (result->value0 == 0)
            result->value0 = result->value2;

        if (result->value1 == 0)
            result->value1 = result->value3;

        if (result->value2 == 0)
            result->value2 = result->value0;

        if (result->value3 == 0)
            result->value3 = result->value1;
    } else {
        result->value3 = 0;
        result->value2 = 0;
    }
}