extern void* DAT_010c59f4;
extern void* DAT_010c6d54;

void __cdecl FUN_00dffe80(void* p, int b)
{
    if (p != 0) {
        *reinterpret_cast<int*>(p) = reinterpret_cast<int>(&DAT_010c59f4);

        if (b != 0) {
            float value = 1.0f;
            int bits = *reinterpret_cast<int*>(&value);
            *reinterpret_cast<unsigned short*>(
                static_cast<char*>(p) + 0x11e) =
                static_cast<unsigned short>(bits >> 16);
        }

        *reinterpret_cast<int*>(p) = reinterpret_cast<int>(&DAT_010c6d54);
    }
}