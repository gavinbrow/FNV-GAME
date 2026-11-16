void __cdecl FUN_00d39060(void* unused, unsigned short* slots, unsigned short value) {
    for (int i = 0; i < 3; ++i) {
        if (slots[i] == 0xffff) {
            slots[i] = value;
            return;
        }
    }
}
