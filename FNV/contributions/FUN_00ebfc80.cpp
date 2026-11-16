unsigned int __cdecl FUN_00ebfc80(unsigned int value)
{
    if (value > 16) {
        if (value > 64) {
            if (value > 128) {
                if (value > 256) {
                    if (value > 512) {
                        return 1024;
                    } else {
                        return 512;
                    }
                } else {
                    return 256;
                }
            } else {
                return 128;
            }
        } else {
            if (value > 32) {
                return 64;
            } else {
                return 32;
            }
        }
    } else {
        if (value > 4) {
            if (value > 8) {
                return 16;
            } else {
                return 8;
            }
        } else {
            if (value > 2) {
                return 4;
            }
        }
    }
    return value;
}
