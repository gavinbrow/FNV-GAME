struct State_c160 { void FUN_00e7f430(unsigned int, unsigned int, bool); };
State_c160* FUN_00e7f5d0();
int FUN_004dc060(int);
extern bool DAT_011f941e, DAT_011f9421;
extern unsigned int DAT_011f9534, DAT_011f948c;
extern float DAT_01200458;
struct Stage_c160 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    void FUN_00e7ecd0();
    void DecRefCount() { --unk60; if (unk60 == 0) FUN_00e7ecd0(); }
};
void FUN_00e7edf0(Stage_c160**);
void FUN_00be0cf0(Stage_c160*, int, int, int, int);
struct StagePtr_c160 {
    Stage_c160* object;
    StagePtr_c160() : object(0) {}
    ~StagePtr_c160() { if (object) object->DecRefCount(); }
};
struct Scope_c160 {
    int previous;
    TLS_bad060* tls;
    Scope_c160() { tls = &tls_bad060; previous = tls->iMemContext; tls->iMemContext = 28; }
    ~Scope_c160() { tls->iMemContext = previous; }
};
struct Pass_c160 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    State_c160* state;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    RefPtr_bacd00 pixel;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    RefPtr_bacd00 vertex;
    void FUN_00e802b0(unsigned int, Stage_c160*);
    void Set(unsigned int key, unsigned int value) { if (!state) state = FUN_00e7f5d0(); state->FUN_00e7f430(key,value,true); }
};
struct Shader_c160 : BSShader {
    Pass_c160* passes[44];
    float value11c;
    unsigned int unk120;
    unsigned int unk124;
    RefObj_bacd00* vertex[24];
    RefObj_bacd00* pixel[7];
    void FUN_00bac160();
};
void Shader_c160::FUN_00bac160() {
    AutoMemContext_bad060 scope(28);
    StagePtr_c160 stage;
    int i;
    for (i = 0; i <= 19; ++i) {
        Pass_c160* pass = passes[i];
        if (pass->unk18 < 1) {
            { FUN_00e7edf0(&stage.object);
            Stage_c160* current = stage.object;
            FUN_00be0cf0(current,0,3,2,0);
            pass->FUN_00e802b0(pass->unk14,current); }
        }
        int pixelIndex;
        if (i >= 8) {
            if (i <= 15) {
            if (pass->unk18 < 3) {
                { FUN_00e7edf0(&stage.object);
                Stage_c160* current = stage.object;
                FUN_00be0cf0(current,1,1,2,0);
                pass->FUN_00e802b0(pass->unk14,current); }
                { FUN_00e7edf0(&stage.object);
                Stage_c160* current = stage.object;
                FUN_00be0cf0(current,2,1,2,0);
                pass->FUN_00e802b0(pass->unk14,current); }
            }
            pixelIndex = 2;
        }
            else pixelIndex = 0;
        } else pixelIndex = 0;
        pass->Set(27,0);
        if (FUN_004dc060(0) >= 2) {
            pass->Set(15,1);
            pass->Set(25,5);
            pass->Set(24,10);
            if (DAT_011f941e && !DAT_011f9421) {
                pass->Set(27,1);
                pass->Set(19,5);
                pass->Set(20,6);
            }
        }
        pass->vertex = vertex[i];
        pass->pixel = pixel[pixelIndex];
    }
    for (i = 20; i <= 39; ++i) {
        Pass_c160* pass = passes[i];
        if (pass->unk18 < 2) {
            { FUN_00e7edf0(&stage.object);
            Stage_c160* current = stage.object;
                FUN_00be0cf0(current,0,3,2,0);
            pass->FUN_00e802b0(pass->unk14,current); }
            { FUN_00e7edf0(&stage.object);
            Stage_c160* current = stage.object;
                FUN_00be0cf0(current,1,3,2,0);
            current->unk08 = DAT_011f9534;
            current->unk0c = 1;
            pass->FUN_00e802b0(pass->unk14,current); }
        }
        int pixelIndex;
        if (i >= 28) {
            if (i <= 35) {
            if (pass->unk18 < 4) {
                { FUN_00e7edf0(&stage.object);
                Stage_c160* current = stage.object;
                FUN_00be0cf0(current,2,1,2,0);
                pass->FUN_00e802b0(pass->unk14,current); }
                { FUN_00e7edf0(&stage.object);
                Stage_c160* current = stage.object;
                FUN_00be0cf0(current,3,1,2,0);
                pass->FUN_00e802b0(pass->unk14,current); }
            }
            pixelIndex = 3;
        }
            else pixelIndex = 1;
        } else pixelIndex = 1;
        if (FUN_004dc060(0) >= 2) {
            pass->Set(15,1);
            pass->Set(25,5);
            pass->Set(24,10);
            if (DAT_011f941e && !DAT_011f9421) {
                pass->Set(27,1);
                pass->Set(19,5);
                pass->Set(20,6);
            }
        } else pass->Set(15,0);
        pass->vertex = vertex[i-20];
        pass->pixel = pixel[pixelIndex];
    }
    for (int j = 0; j < 4; ++j) {
        Pass_c160* pass = passes[j+40];
        if (pass->unk18 < 2) {
            { FUN_00e7edf0(&stage.object);
            Stage_c160* current = stage.object;
                FUN_00be0cf0(current,0,3,2,0);
            pass->FUN_00e802b0(pass->unk14,current); }
            { FUN_00e7edf0(&stage.object);
            Stage_c160* current = stage.object;
                FUN_00be0cf0(current,1,3,2,0);
            pass->FUN_00e802b0(pass->unk14,current); }
        }
        pass->Set(27,1);
        pass->Set(19,9);
        pass->Set(20,1);
        pass->Set(14,0);
        float value = DAT_01200458;
        pass->Set(195, *reinterpret_cast<unsigned int*>(&value));
        pass->Set(152,63);
        pass->vertex = vertex[j+20];
        pass->pixel = pixel[DAT_011f948c+4];
    }
}
