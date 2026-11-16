struct WriteStream {void* unk00; unsigned int transferred;void* unk08;int (__cdecl *write)(WriteStream*,const void*,unsigned int,unsigned int*,int);};
struct BufferOwner {void* unk00; unsigned char* buffer; void __thiscall FUN_00c8a280(void*);void __thiscall FUN_00cbdf10(void*);};
void BufferOwner::FUN_00cbdf10(void* source) {
 FUN_00c8a280(source);
 unsigned char* data=buffer;
 WriteStream* __restrict stream=*(WriteStream**)((unsigned char*)source+0x250);
 unsigned int length=64;
 stream->transferred+=stream->write(stream,data+0x20,64,&length,1);
 stream=*(WriteStream**)((unsigned char*)source+0x250);
 length=64;
 stream->transferred+=stream->write(stream,data+0x60,64,&length,1);
}