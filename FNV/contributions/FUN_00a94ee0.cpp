
struct BinaryWriter;
typedef int (__cdecl *WriteProc)(BinaryWriter*, const void*, unsigned int, unsigned int*, int);
struct BinaryWriter {
 int unk00; unsigned int byteCount; int unk08; WriteProc callback;
 __forceinline int WriteValue(const void* data) { unsigned int length = 4; return callback(this, data, 4, &length, 1); }
};
struct NiStreamArg { BinaryWriter* writer() { return *(BinaryWriter**)((char*)this+0x250); } };
struct LightBaseSerialization { void FUN_00a7d8d0(NiStreamArg* stream); };
struct LightSerialization { void FUN_00a94ee0(NiStreamArg* stream); };
void LightSerialization::FUN_00a94ee0(NiStreamArg* stream) {
 ((LightBaseSerialization*)this)->FUN_00a7d8d0(stream);
 NiSpotLight* spot=(NiSpotLight*)this;
 unsigned int bytes;
 BinaryWriter* output=stream->writer();
 output->byteCount += output->WriteValue(&spot->m_f0108);
 output=stream->writer();
 output->byteCount += output->WriteValue(&spot->m_f010c);
 output=stream->writer();
 output->byteCount += output->WriteValue(&spot->m_f0110);
}
