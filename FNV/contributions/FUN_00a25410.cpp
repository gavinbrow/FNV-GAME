
extern unsigned char DAT_011f35ae;
extern unsigned char DAT_011f35af;
extern unsigned short DAT_011f35b0;
extern unsigned short DAT_011f35b2;
extern unsigned short DAT_011f35b4;
extern unsigned short DAT_011f35b6;

void InputManager::FUN_00a25410(int offset) {
    for (int i = 0; i < 4; ++i) {
        if (reinterpret_cast<unsigned char*>(this)[i * 28 + offset + 0x1b94] == 0xff) {
            continue;
        }
        switch (i) {
        case 0:
            reinterpret_cast<unsigned char*>(this)[0x18f8 + reinterpret_cast<unsigned char*>(this)[i * 28 + offset + 0x1b94]] = 0;
            break;
        case 1:
            reinterpret_cast<unsigned char*>(this)[0x1b30 + reinterpret_cast<unsigned char*>(this)[i * 28 + offset + 0x1b94]] = 0;
            break;
        case 2:
            if (reinterpret_cast<unsigned char*>(this)[i * 28 + offset + 0x1b94] < 32) {
                reinterpret_cast<unsigned char*>(this)[0x64 + reinterpret_cast<unsigned char*>(this)[i * 28 + offset + 0x1b94]] = 0;
            } else {
                reinterpret_cast<unsigned int*>(reinterpret_cast<unsigned char*>(this) + 0x54)[
                    static_cast<unsigned short>((static_cast<unsigned int>(reinterpret_cast<unsigned char*>(this)[i * 28 + offset + 0x1b94]) >> 16) & 0xffff)] = 0;
            }
            break;
        }
    }
    DAT_011f35ae=0; DAT_011f35af=0;
    DAT_011f35b0=0; DAT_011f35b2=0;
    DAT_011f35b4=0; DAT_011f35b6=0;
    DAT_011f35ac=0;
}
