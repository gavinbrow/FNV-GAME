struct ComponentValue {
    int value;
    int unk04;
};

struct Target : FUN_00d2c3a0_class {
    int unk0C;
    ComponentValue values[16];
    int terminal;
    volatile int weights[17];
    int FUN_00d2c350();
};

int Target::FUN_00d2c350()
{
    int firstSum = 0;
    int secondSum = 0;
    int* firstValue = &values[1].value;
    volatile int* secondWeight = &weights[1];
    int remaining = 8;
    do {
        firstSum += secondWeight[-1] * firstValue[-2];
        secondSum += secondWeight[0] * firstValue[0];
        secondWeight += 2;
        firstValue += 4;
        --remaining;
    } while (remaining != 0);
    int result = firstSum;
    result += secondSum;
    result += terminal * weights[16];
    return result;
}

