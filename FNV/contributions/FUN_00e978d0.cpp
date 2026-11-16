struct D3DPixelShader;
struct PixelShaderInterface {
    virtual void Slot00();
    virtual void Slot01();
    virtual void Slot02();
    virtual void Slot03();
    virtual void Slot04();
    virtual void Slot05();
    virtual void Slot06();
    virtual void Slot07();
    virtual void Slot08();
    virtual void Slot09();
    virtual void Slot10();
    virtual void Slot11();
    virtual void Slot12();
    virtual void Slot13();
    virtual void Slot14();
    virtual void Slot15();
    virtual void Slot16();
    virtual void Slot17();
    virtual void Slot18();
    virtual void Slot19();
    virtual void Slot20();
    virtual void Slot21();
    virtual void Slot22();
    virtual void Slot23();
    virtual void Slot24();
    virtual D3DPixelShader* GetPixelShader();
    virtual void Slot26();
    virtual void Slot27();
    virtual void Slot28();
    virtual void Slot29();
    virtual void Slot30();
    virtual void* GetShaderData();
    virtual void Slot32();
    virtual void Slot33();
    virtual void SetShaderProgram(void*);
    virtual void* GetShaderProgram();
};
struct PixelShaderCreator {
    void* FUN_00e98890(D3DPixelShader*, void**, void*, int, int, int);
    bool FUN_00e978d0(PixelShaderInterface*);
};
bool PixelShaderCreator::FUN_00e978d0(PixelShaderInterface* shader) {
    D3DPixelShader* pixel = shader->GetPixelShader();
    if (!pixel)
        return false;
    void* program = shader->GetShaderProgram();
    void* created = FUN_00e98890(pixel, &program, shader->GetShaderData(), 0, 0, 0);
    if (!created)
        return false;
    shader->SetShaderProgram(created);
    return true;
}