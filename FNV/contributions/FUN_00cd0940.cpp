void __cdecl FUN_00d2cab0(void*, int, unsigned int);
struct FUN_00cd0940_record {
    virtual void slot00() = 0; virtual void slot01() = 0; virtual void slot02() = 0; virtual void slot03() = 0;
    virtual void slot04() = 0; virtual void slot05() = 0; virtual void slot06() = 0; virtual void slot07() = 0;
    virtual void slot08() = 0; virtual void slot09() = 0; virtual void slot10() = 0; virtual void slot11() = 0;
    virtual void slot12() = 0; virtual void slot13() = 0;
};
struct FUN_00cd0940_iface { virtual void slot00() = 0; virtual void slot01() = 0; virtual void slot02(int, int) = 0; };
struct FUN_00cd0940_shell { void __thiscall FUN_00cd0940(int* param, unsigned char mode); };
void __thiscall FUN_00cd0940_shell::FUN_00cd0940(int* param, unsigned char mode)
{
    FUN_00cd0940_record* record = (FUN_00cd0940_record*)((unsigned char*)this + param[8] * 0x138 + 0xc6c);
    if ((mode & 2) != 0) {
        if (*(int*)((unsigned char*)record + 0x130) != 0) {
            int start = param[1];
            int length = param[2] - start;
            if (length != 0) {
                ((FUN_00cd0940_iface*)((unsigned char*)this + 0x1c))->slot02(start, length);
                param[1] = 0; param[0] = 0; param[2] = 0;
            }
        }
        record->slot13();
        param[3] = 0; param[6] = 0;
    }
    if ((mode & 1) != 0) {
        record->slot13();
        *(volatile int*)((unsigned char*)record + 0x128) = 0;
        *(volatile unsigned char*)((unsigned char*)record + 0x12c) = 0;
        FUN_00d2cab0(param, 0, 0x24);
    }
}
