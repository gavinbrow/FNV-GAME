struct NiPoint3Ex;
struct NiPoint3;
struct M3 { float m[9]; };
struct Frus { float f[7]; };
struct NiUpdateData {
    float a; int b; int c;
    NiUpdateData(float, bool, bool);
};
struct Host56 {
    M3 FUN_0056fa00();
};
struct Rot56 {
};
struct Node60 {
    const NiPoint3& FUN_0045bb80();
    Host56* FUN_006a9540();
};
struct Prop {
    const Frus& FUN_0045bbe0();
};
struct Anim {
    const Frus& FUN_0045bbe0();
    void FUN_00a6faf0(Frus*);
};
struct MidX {
    Anim* FUN_006629f0();
};
struct Node6c {
    void FUN_00a59c60(const NiUpdateData&);
    const NiPoint3& FUN_0043c490();
    Prop* FUN_0045bc00(int);
};
struct NiPtr60 {
    Node60* FUN_00559450();
};
struct NiPtr6c {
    Node6c* FUN_00559450();
};
struct Rend {
    unsigned int FUN_004dee10();
    unsigned int FUN_004dee70();
};
Rend* __cdecl FUN_0043c4b0();
MidX* __cdecl FUN_0045c670();
struct BSAudio;
struct BSSoundHandleEx {
    int a; int b; int c;
    ~BSSoundHandleEx();
    bool FUN_00ad8830(bool);
};
struct BSAudio {
    BSSoundHandleEx FUN_00ad7550(const char*, int);
};
BSAudio* __cdecl FUN_00453a70();
struct GObj {
    virtual void w000();
    virtual void w001();
    virtual void w002();
    virtual void w003();
    virtual void w004();
    virtual void w005();
    virtual void w006();
    virtual void w007();
    virtual void w008();
    virtual void w009();
    virtual void w010();
    virtual void w011();
    virtual void w012();
    virtual void w013();
    virtual void w014();
    virtual void w015();
    virtual void w016();
    virtual void w017();
    virtual void w018();
    virtual void w019();
    virtual void w020();
    virtual void w021();
    virtual void w022();
    virtual void w023();
    virtual void w024();
    virtual void w025();
    virtual void w026();
    virtual void w027();
    virtual void w028();
    virtual void w029();
    virtual void w030();
    virtual void w031();
    virtual void w032();
    virtual void w033();
    virtual void w034();
    virtual void w035();
    virtual void w036();
    virtual void w037();
    virtual void w038();
    virtual void w039();
    virtual void w040();
    virtual void w041();
    virtual void w042();
    virtual void w043();
    virtual void w044();
    virtual void w045();
    virtual void w046();
    virtual void w047();
    virtual void w048();
    virtual void w049();
    virtual void w050();
    virtual void w051();
    virtual void w052();
    virtual void w053();
    virtual void w054();
    virtual void w055();
    virtual void w056();
    virtual void w057();
    virtual void w058();
    virtual void w059();
    virtual void w060();
    virtual void w061();
    virtual void w062();
    virtual void w063();
    virtual void w064();
    virtual void w065();
    virtual void w066();
    virtual void w067();
    virtual void w068();
    virtual void w069();
    virtual void w070();
    virtual void w071();
    virtual void w072();
    virtual void w073();
    virtual void w074();
    virtual void w075();
    virtual void w076();
    virtual void w077();
    virtual void w078();
    virtual void w079();
    virtual void w080();
    virtual void w081();
    virtual void w082();
    virtual void w083();
    virtual void w084();
    virtual void w085();
    virtual void w086();
    virtual void w087();
    virtual void w088();
    virtual void w089();
    virtual void w090();
    virtual void w091();
    virtual void w092();
    virtual void w093();
    virtual void w094();
    virtual void w095();
    virtual void w096();
    virtual void w097();
    virtual void w098();
    virtual void w099();
    virtual void w100();
    virtual void w101();
    virtual void w102();
    virtual void w103();
    virtual void w104();
    virtual void w105();
    virtual void w106();
    virtual void w107();
    virtual void w108();
    virtual void w109();
    virtual void w110();
    virtual void w111();
    virtual void w112();
    virtual void w113();
    virtual void w114();
    virtual void w115();
    virtual void w116();
    virtual void w117();
    virtual void w118();
    virtual void w119();
    virtual void w120();
    virtual void w121();
    virtual void w122();
    virtual void w123();
    virtual void w124();
    virtual void w125();
    virtual void w126();
    virtual void w127();
    virtual void w128();
    virtual void w129();
    virtual void w130();
    virtual void w131();
    virtual void w132();
    virtual void w133();
    virtual void w134();
    virtual void w135();
    virtual void w136();
    virtual void w137();
    virtual void w138();
    virtual bool Check22c(int);
    void FUN_00950110(int);
    void FUN_0094a0c0(NiPoint3*, NiPoint3*, int);
};
class LenShell;
class PtOp {
public:
    float x; float y; float z;
    NiPoint3 operator-(const NiPoint3&) const;
    LenShell* FUN_00439ef0();
};

class NiPoint3_helper {
public:
    NiPoint3Ex operator*(float) const;
};
class PtSub {
public:
    NiPoint3& operator-=(const NiPoint3&);
};
class PtTest {
public:
    bool FUN_004390c0(const NiPoint3&);
};
class LenShell {
public:
    float FUN_00457990();
};
float* __fastcall FUN_00403e20(void*);
void __cdecl FUN_00a582f0(const M3&, void*, int, NiPoint3&, NiPoint3&);
void __cdecl FUN_00a582f0(Host56*, void*, int, NiPoint3&, NiPoint3&);
extern NiPoint3 DAT_011ca77c;
extern NiPoint3 DAT_011ca75c;
extern NiPoint3 DAT_011e0808;
extern NiPoint3 DAT_011ca7a8;
extern NiPoint3 DAT_011f426c;
extern float DAT_011ca72c;
extern float DAT_011ca730;
extern float DAT_011ca734;
extern unsigned char DAT_011ca728;
extern unsigned char DAT_011ca729;
extern GObj* DAT_011dea3c;
extern Host56* DAT_011f21f0;
extern float DAT_011ca76c;
extern float DAT_011ca7d0;
struct NiPoint3Ex {
    float x; float y; float z;
    NiPoint3Ex operator-(const NiPoint3&) const;
    NiPoint3Ex operator+(const NiPoint3Ex&) const;
    float Length() const;
};
struct Shot {
    int f00[14];
    int f38;
    int f3c;
    int f40[8];
    NiPtr60 m60;
    int f64;
    Host56* f68;
    NiPtr6c m6c;
    int f70;
    char c74;
    unsigned char c75;
    char c76;
    char c77;
    bool FUN_0058ccd0();
    bool FUN_0058d4f0();
    NiPoint3Ex FUN_0058d510();
    void FUN_0058cf60(float);
};
void Shot::FUN_0058cf60(float t)
{
    if (!m6c.FUN_00559450())
        return;
    NiUpdateData upd(t, true, false);
    m6c.FUN_00559450()->FUN_00a59c60(upd);
    DAT_011ca77c = m6c.FUN_00559450()->FUN_0043c490();
    NiPoint3 pt = DAT_011ca77c;
    if (c75 && !DAT_011dea3c->Check22c(0))
        DAT_011dea3c->FUN_00950110(1);
    else
    {
        if (FUN_0058ccd0())
        {
            if (!FUN_0058d4f0() || f68 == 0 || f3c != 2)
            {
                NiPoint3 tmpA = pt;
                FUN_00a582f0(DAT_011f21f0->FUN_0056fa00(), &DAT_011f426c, 1, tmpA, pt);
            }
            else
            {
                NiPoint3 tmpB = pt;
                FUN_00a582f0(f68->FUN_0056fa00(), &DAT_011f426c, 1, tmpB, pt);
            }
        }
        else if (m60.FUN_00559450())
        {
            NiPoint3 tmpC = pt;
            FUN_00a582f0(m60.FUN_00559450()->FUN_006a9540(), &DAT_011f426c, 1, tmpC, pt);
        }
        if (m60.FUN_00559450())
        {
            bool bReset = false;
            if (((PtTest*)&DAT_011ca75c)->FUN_004390c0(DAT_011f426c))
            {
                DAT_011ca75c = DAT_011e0808;
                bReset = true;
            }
            NiPoint3 kPos = m60.FUN_00559450()->FUN_0045bb80();
            ((PtSub*)&pt)->operator-=(kPos);
            DAT_011dea3c->FUN_0094a0c0(&pt, &kPos, 0);
            DAT_011e0808 = pt;
            if (DAT_011ca728)
            {
                *(NiPoint3Ex*)&DAT_011ca7a8 = *(NiPoint3Ex*)&DAT_011e0808 - DAT_011ca75c;
                if (((NiPoint3Ex*)&DAT_011ca7a8)->Length() <= *FUN_00403e20(&DAT_011ca76c))
                {
                    DAT_011ca728 = 0;
                    DAT_011ca72c = 0.0f;
                }
                else if (f38 == 0)
                {
                    DAT_011ca728 = 0;
                    DAT_011ca72c = 0.0f;
                }
                else
                {
                    if (bReset && !DAT_011ca729)
                    {
                        BSSoundHandleEx snd = FUN_00453a70()->FUN_00ad7550("UIVATSCameraIn", 0x121);
                        snd.FUN_00ad8830(false);
                    }
                    DAT_011ca730 = (1.0f / DAT_011ca734) * (t - DAT_011ca72c);
                    if (DAT_011ca730 >= 1.0)
                    {
                        DAT_011ca728 = 0;
                        DAT_011ca72c = 0.0f;
                    }
                    else
                        *(NiPoint3Ex*)&DAT_011e0808 = *(NiPoint3Ex*)&DAT_011ca75c + ((NiPoint3_helper*)&DAT_011ca7a8)->operator*(DAT_011ca730);
                }
            }
            Prop* pCam = m6c.FUN_00559450()->FUN_0045bc00(0);
            if (pCam)
            {
                Frus kOrigFrustum = pCam->FUN_0045bbe0();
                Anim* pMainCamera = FUN_0045c670()->FUN_006629f0();
                Frus kFrustum = pMainCamera->FUN_0045bbe0();
                float scale = (double)FUN_0043c4b0()->FUN_004dee10() / (double)FUN_0043c4b0()->FUN_004dee70() / 1.3333334f;
                kFrustum.f[0] = kOrigFrustum.f[0] * scale;
                kFrustum.f[1] = kOrigFrustum.f[1] * scale;
                kFrustum.f[2] = kOrigFrustum.f[2];
                kFrustum.f[3] = kOrigFrustum.f[3];
                pMainCamera->FUN_00a6faf0(&kFrustum);
            }
        }
    }
    if ((FUN_0058d510() - pt).Length() <= *FUN_00403e20(&DAT_011ca7d0))
        c75 = 1;
}
