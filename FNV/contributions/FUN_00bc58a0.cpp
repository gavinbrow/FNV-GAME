struct FUN_00be2200 {
    virtual ~FUN_00be2200();
    unsigned int m_state04;
    unsigned int m_state08;
    unsigned int m_state0c;
    unsigned int m_state10;
    unsigned int m_state14;
    unsigned int m_state18;
    unsigned int m_state1c;
    unsigned int m_state20;
    unsigned int m_state24;
    unsigned int m_state28;
    unsigned int m_state2c;
    unsigned int m_state30;
    unsigned int m_state34;
    unsigned int m_state38;
    unsigned int m_state3c;
    unsigned int m_state40;
    unsigned int m_state44;
    unsigned int m_state48;
    unsigned int m_state4c;
    unsigned int m_state50;
    unsigned int m_state54;
    unsigned int m_state58;
    unsigned int m_state5c;
    unsigned int m_state60;
    unsigned int m_state64;
    volatile unsigned int m_shaderStage;
    FUN_00be2200();
};
struct ShaderValue {
    unsigned int m_value;
    ShaderValue();
};
struct InputShaderValue : ShaderValue { ~InputShaderValue(); };
struct OutputShaderValue : ShaderValue { ~OutputShaderValue(); };
struct FUN_00bc58a0 : FUN_00be2200 {
    InputShaderValue m_inputValues[3];
    OutputShaderValue m_outputValues[2];
    OutputShaderValue m_auxiliaryValues[2];
    float m_constants[8];
    FUN_00bc58a0();
    virtual ~FUN_00bc58a0();
};
FUN_00bc58a0::FUN_00bc58a0() {
    m_constants[7] = m_constants[6] = m_constants[5] = m_constants[4] =
    m_constants[3] = m_constants[2] = m_constants[1] = m_constants[0] = 0.0f;
    m_shaderStage = 19;
}