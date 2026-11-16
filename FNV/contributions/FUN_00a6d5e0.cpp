struct NiTimeController_Luna : NiTimeController {void FUN_00a6d5e0(NiStream& kStream);};
void NiTimeController_Luna::FUN_00a6d5e0(NiStream& kStream) {
NiObject::LoadBinary(kStream);kStream.ReadLinkID();
NiStreamLoadBinary(kStream,m_uFlags);NiStreamLoadBinary(kStream,m_fFrequency);
NiStreamLoadBinary(kStream,m_fPhase);NiStreamLoadBinary(kStream,m_fLoKeyTime);
NiStreamLoadBinary(kStream,m_fHiKeyTime);kStream.ReadLinkID();
if(kStream.GetFileVersion()<0x0A000101) {unsigned short preserved = m_uFlags; m_uFlags &= 0xFFF0; m_uFlags *= 2; m_uFlags |= preserved & 0xF;}
if(kStream.GetFileVersion()<0x0A000103){kStream.m_usNiTimeControllerFlags=m_uFlags;m_uFlags&=0x001F;}
if(kStream.GetFileVersion()<0x0A01006D)m_uFlags&=0xFFDF;
m_uFlags=(m_uFlags&0xFF7F)|0x40;}