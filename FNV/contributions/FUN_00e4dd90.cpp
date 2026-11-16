struct FUN_00e4dd90_shell { void __thiscall FUN_00e4dd90(float* output); };
void __thiscall FUN_00e4dd90_shell::FUN_00e4dd90(float* output)
{
    if (*(int*)((unsigned char*)this + 0x0c) != 0) {
        output[0] = *(float*)(*(unsigned char**)(*(unsigned char**)((unsigned char*)this + 0x0c) + 0xc4) + 0x10);
        output[1] = *(float*)(*(unsigned char**)(*(unsigned char**)((unsigned char*)this + 0x0c) + 0xc4) + 0x70);
        output[2] = *(float*)(*(unsigned char**)(*(unsigned char**)((unsigned char*)this + 0x0c) + 0xc4) + 0xd0);
        output[3] = *(float*)(*(unsigned char**)(*(unsigned char**)((unsigned char*)this + 0x0c) + 0xc4) + 0x130);
    }
}
