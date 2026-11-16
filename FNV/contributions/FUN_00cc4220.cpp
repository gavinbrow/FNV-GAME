#include "h_74712c1d3c73.h"

struct FUN_00cc4220_source {
    float unk00;
    float unk04;
    float unk08;
    float unk0c;
    float m_f10;
    float m_f14;
    float m_f18;
    float m_f1c;
    float m_f20;
    float m_f24;
    float m_f28;
    float m_f2c;
    float m_f30;
    float m_f34;
};

struct FUN_00cc4220_output {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    float m_f10;
    float m_f14;
    float m_f18;
    float m_f1c;
    float m_f20;
    float m_f24;
};

struct FUN_00cc4220_class {
    void* unk00;
    void* unk04;
    FUN_00cc4220_source* m_p;

    void __thiscall FUN_00c8a800(void* p);
    void __thiscall FUN_00cc4220(void* p);
};

extern "C" float DAT_012683b0[4];

void __thiscall FUN_00cc4220_class::FUN_00cc4220(void* p)
{
    FUN_00cc4220_output* out = static_cast<FUN_00cc4220_output*>(p);

    this->FUN_00c8a800(p);

    float value = (this != 0 && this->m_p != 0)
        ? this->m_p->m_f34
        : 0.0f;
    out->m_f24 = value;

    const float* values = (this != 0 && this->m_p != 0)
        ? &this->m_p->m_f20
        : DAT_012683b0;

    out->m_f10 = values[0];
    out->m_f14 = values[1];
    out->m_f18 = values[2];
    out->m_f1c = values[3];

    float position = (this != 0 && this->m_p != 0)
        ? this->m_p->m_f30
        : 0.0f;
    out->m_f20 = position;
}