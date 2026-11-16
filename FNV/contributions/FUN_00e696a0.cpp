struct VertexDeclarationElement { unsigned short stream,offset; unsigned char type,method,usage,usageIndex; };
struct VertexDeclarationDevice : Dev { virtual long __stdcall DrawPrimitiveUP(); virtual long __stdcall DrawIndexedPrimitiveUP(); virtual long __stdcall ProcessVertices(); virtual long __stdcall CreateVertexDeclaration(const VertexDeclarationElement*, void**); };
struct RendererDeclarationOwner { unsigned int m_rendererFields[0xa0]; void* m_vertexDeclaration; unsigned int m_declarationState; VertexDeclarationDevice* m_device; void* __thiscall FUN_00e696a0(); };
void* RendererDeclarationOwner::FUN_00e696a0() {
 if (!m_vertexDeclaration) {
    VertexDeclarationElement elements[5] = { {0,0,2,0,0,0}, {0,12,2,0,3,0}, {0,24,4,0,10,0}, {0,28,1,0,5,0}, {255,0,17,0,0,0} };
    if (m_device->CreateVertexDeclaration(elements, &m_vertexDeclaration) < 0) m_vertexDeclaration = 0;
 }
 return m_vertexDeclaration;
}