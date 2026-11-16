struct PropertyFlagWord { unsigned short value; void Merge(unsigned bits) { unsigned short retained = value; retained &= 0xfff9; retained |= (unsigned short)(bits * 2); value = retained; } };
struct Reader { unsigned unk00; unsigned position; typedef int (__cdecl *ReadFn)(Reader*,void*,unsigned,unsigned*,unsigned); ReadFn read; };
struct LoadStream {
 unsigned version() const { return *(const unsigned*)((const char*)this+0xd8); }
 unsigned short legacyFlags() const { return *(const unsigned short*)((const char*)this+0x288); }
 Reader* reader() const { return *(Reader*const*)((const char*)this+0x24c); }
};
void __stdcall FUN_00a5d7f0(LoadStream*);
struct SubObject { void FUN_00a59be0(LoadStream*); };
struct NiPropertyData {
 unsigned short& flags() { return *(unsigned short*)((char*)this+0x18); }
 unsigned& extra() { return *(unsigned*)((char*)this+0x1c); }
 void FUN_00a9a150(LoadStream*);
};
void NiPropertyData::FUN_00a9a150(LoadStream* stream) {
 LoadStream* original = stream;
 FUN_00a5d7f0(original);
 if (original->version() < 0x0a000102) {
   unsigned raw = original->legacyFlags();
   flags() = (unsigned short)raw;
   if (original->version() < 0x05000016) {
     unsigned char bit = (unsigned char)raw;
     bit >>= 1;
     bit &= 1;
     raw >>= 3;
     raw &= 3;
     flags() = 0;
     if (bit) flags() = 1;
     else flags() = 0;
     ((PropertyFlagWord*)((char*)this+0x18))->Merge(raw);
   } else {
     flags() = (unsigned short)(raw & 7);
   }
 } else {
   Reader* rd = original->reader();
   Reader::ReadFn fn = rd->read;
   unsigned& amount = *(unsigned*)&stream;
   amount = 2;
   int count = fn(rd,&flags(),2,&amount,1);
   rd->position += count;
 }
 Reader* rd = original->reader();
 Reader::ReadFn fn = rd->read;
 unsigned& amount = *(unsigned*)&stream;
 amount = 4;
 int count = fn(rd,&extra(),4,&amount,1);
 rd->position += count;
 ((SubObject*)((char*)this+0x20))->FUN_00a59be0(original);
}