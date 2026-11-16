struct InputStream { unsigned char* ptr; int count; };
extern int __cdecl FUN_00edc81f(InputStream*);
// @fnv 0x00eda0cb
unsigned int __fastcall FUN_00eda0cb(int, InputStream* stream) { --stream->count; if (stream->count >= 0) { return *stream->ptr++; } return FUN_00edc81f(stream); }
