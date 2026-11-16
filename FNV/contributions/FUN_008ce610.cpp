

struct SaveStream {

    int __thiscall FUN_00825c00();

    bool __thiscall FUN_00862110();

    unsigned char __thiscall FUN_008df040();

    void __thiscall FUN_008579b0(const void*, int);

    void* __thiscall FUN_004fd3e0();

};

struct SaveFlag {

    unsigned char* __thiscall FUN_00408d60();

};

extern SaveFlag DAT_011de4e8;

extern unsigned char UNK_0101536c, UNK_010153a0, UNK_01015318, UNK_01085d58;

extern "C" void __cdecl FUN_0040fbe0(const void*, ...);

extern "C" void __cdecl FUN_005b5e40(const void*, const void*, int);

extern "C" int __cdecl FUN_004839c0(int);

extern "C" int __cdecl FUN_004a8b00(int);

extern "C" unsigned short __cdecl FUN_004b66d0(int, int, int, int);

extern "C" unsigned short __cdecl FUN_004b6810(int, int, int, int, int);

struct SaveHandle {

    int __thiscall FUN_0084e3a0();

};

struct StateProcessor {

    int __thiscall FUN_0043fcd0();

};

struct Vec3f { float x, y, z; };

struct EmitState {

    int type;

    Vec3f origin;

    Vec3f axis;

    Vec3f velocity;

    StateProcessor* handle;

    int packed;

    char extended[16];

};

struct FourInts {

    int x0,x1,x2,x3;

    void __thiscall FUN_006815c0();

    void __thiscall FUN_00a6df40(void*);

};

struct FUN_008ce610_owner : PC7d {

    void __thiscall FUN_00932070(int);

    void __thiscall FUN_00484d20(void*, int);

    void __thiscall FUN_008ce610(int);

};

void FUN_008ce610_owner::FUN_008ce610(int arg) {

    FUN_00932070(arg);

    unsigned short idB = 0;

    unsigned short* pLength = 0;

    int start = reinterpret_cast<SaveStream*>(DAT_011de45c)->FUN_00825c00();

    if (*DAT_011de4e8.FUN_00408d60()) {

        start = reinterpret_cast<SaveStream*>(DAT_011de45c)->FUN_00825c00();

    }

    if (reinterpret_cast<SaveStream*>(DAT_011de45c)->FUN_00862110()) {

        unsigned int magic = 0x424c4f4b;

        reinterpret_cast<TESSaveLoadGameHelper*>(DAT_011de45c)->FUN_008579b0(&magic, 4);

        pLength = reinterpret_cast<unsigned short*>(reinterpret_cast<SaveStream*>(DAT_011de45c)->FUN_00825c00());

        reinterpret_cast<TESSaveLoadGameHelper*>(DAT_011de45c)->FUN_008579b0(&idB, 2);

    }

    reinterpret_cast<TESSaveLoadGameHelper*>(DAT_011de45c)->FUN_008579b0(reinterpret_cast<char*>(this)+0x8c,4);

    FUN_00484ce0(reinterpret_cast<char*>(this)+0x90,4);

    FUN_00484ce0(reinterpret_cast<char*>(this)+0x94,4);

    FUN_00484ce0(reinterpret_cast<char*>(this)+0x98,4);

    FUN_00484ce0(reinterpret_cast<char*>(this)+0x9c,4);

    FUN_00484ce0(reinterpret_cast<char*>(this)+0xa0,4);

    FUN_00484ce0(reinterpret_cast<char*>(this)+0xb4,12);

    unsigned int hasState = 0;

    if (*reinterpret_cast<SaveHandle**>(reinterpret_cast<char*>(this)+0xa4)) hasState = (*reinterpret_cast<SaveHandle**>(reinterpret_cast<char*>(this)+0xa4))->FUN_0084e3a0();

    FUN_00484d20(&hasState,4);

    unsigned int idA = 0;

    if (*reinterpret_cast<SaveHandle**>(reinterpret_cast<char*>(this)+0xa8)) idA = (*reinterpret_cast<SaveHandle**>(reinterpret_cast<char*>(this)+0xa8))->FUN_0084e3a0();

    FUN_00484d20(&idA,4);

    unsigned int blockLength = 0;

    if (*reinterpret_cast<SaveHandle**>(reinterpret_cast<char*>(this)+0xb0)) blockLength = (*reinterpret_cast<SaveHandle**>(reinterpret_cast<char*>(this)+0xb0))->FUN_0084e3a0();

    FUN_00484d20(&blockLength,4);

    bool idC = false;

    if (*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88)) idC = true;

    FUN_00484ce0(&idC,1);

    if (idC) {

        reinterpret_cast<TESSaveLoadGameHelper*>(DAT_011de45c)->FUN_008579b0((*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88)),4);

        FUN_00484ce0(&(*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->origin,12);

        FUN_00484ce0(&(*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->axis,12);

        FUN_00484ce0(&(*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->velocity,12);

        if (DAT_011de45c->FUN_008df040() >= 0x50) {

            FourInts transform;

            transform.FUN_006815c0();

            transform.FUN_00a6df40(&(*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->extended);

            reinterpret_cast<TESSaveLoadGameHelper*>(DAT_011de45c)->FUN_008579b0(&transform,16);

        }

        if ((*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->type == 1 || (*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->type == 0) {

            unsigned int handleID = 0;

            if ((*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->handle) handleID = reinterpret_cast<SaveHandle*>((*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->handle)->FUN_0084e3a0();

            FUN_00484d20(&handleID,4);

            unsigned short low = 0;

            short high = -1;

            if ((*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->handle && (*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->packed) {

                if (*reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this)+0xc0) == 0) {

                    bool invert = (*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->type == 0;

                    low = FUN_004b66d0((*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->handle->FUN_0043fcd0(),invert,invert,1);

                    int prepared = FUN_004a8b00((*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->packed);

                    high = FUN_004b6810((*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->handle->FUN_0043fcd0(),prepared,invert,invert,1);

                } else {

                    unsigned int packedValue = (*reinterpret_cast<EmitState**>(reinterpret_cast<char*>(this)+0x88))->packed;

                    low = static_cast<unsigned short>(packedValue >> 16);

                    high = static_cast<unsigned short>((packedValue << 16) >> 16);

                }

            }

            FUN_00484ce0(&low,2);

            FUN_00484ce0(&high,2);

        }

    }

    if (DAT_011de45c->FUN_008df040() >= 0x54) {

        FUN_00484ce0(reinterpret_cast<char*>(this)+0xc1,1);

    }

    if (DAT_011de45c->FUN_008df040() >= 0x55) {

        FUN_00484ce0(reinterpret_cast<char*>(this)+0xc2,1);

    }

    if (*DAT_011de4e8.FUN_00408d60()) {

        int info = reinterpret_cast<SaveStream*>(DAT_011de45c)->FUN_00825c00();

        unsigned int* finished = static_cast<unsigned int*>(reinterpret_cast<SaveStream*>(DAT_011de45c)->FUN_004fd3e0());

        if (finished) {

            int manager = FUN_004839c0(*finished);

            typedef int (__thiscall *LogFunction)(void*);

            FUN_0040fbe0(&UNK_010153a0, info-start, *finished,

                reinterpret_cast<LogFunction>((*reinterpret_cast<void***>(manager))[76])(reinterpret_cast<void*>(manager)),

                *reinterpret_cast<int*>(reinterpret_cast<char*>(finished)+5), 0x8ea, &UNK_01085d58);

        } else {

            FUN_0040fbe0(&UNK_0101536c,info-start,0x8ea,&UNK_01085d58);

        }

    }

    if (reinterpret_cast<SaveStream*>(DAT_011de45c)->FUN_00862110()) {

        int lengthFieldPointer = reinterpret_cast<SaveStream*>(DAT_011de45c)->FUN_00825c00();

        unsigned short* info = pLength;

        if (static_cast<unsigned int>(lengthFieldPointer) > reinterpret_cast<unsigned int>(info)+0xffffU) {

            FUN_005b5e40(&UNK_01015318,&UNK_01085d58,0x8ea);

        }

        *pLength = static_cast<unsigned short>(lengthFieldPointer - reinterpret_cast<int>(info));

    }

}

