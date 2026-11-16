struct NiParticlesDataWriter : NiParticlesData { void __thiscall FUN_00a97290(NiStream&); };
struct NiPSysDataWriter : NiParticlesDataWriter {
    NiParticleInfo* particleInfo;
    float* rotationSpeeds;
    void __thiscall FUN_00c25560(NiStream&);
};
void NiPSysDataWriter::FUN_00c25560(NiStream& stream)
{
    NiParticlesDataWriter::FUN_00a97290(stream);
    bool hasRotationSpeeds = rotationSpeeds != 0;
    NiBinaryStream* output = stream.m_pkOstr;
    unsigned int (__cdecl *writer)(NiBinaryStream*, const void*, unsigned int, unsigned int*, unsigned int) = output->m_pfnWrite;
    unsigned int count = 1;
    output->m_uiAbsoluteCurrentPos += writer(output, &hasRotationSpeeds, 1, &count, 1);
}