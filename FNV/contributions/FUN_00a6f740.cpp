struct Writer;struct Stream{Writer* writer()const{return *reinterpret_cast<Writer* const*>(reinterpret_cast<const char*>(this)+0x250);}};
struct Writer{void* handler0;unsigned int bytesWritten;void* handler8;unsigned int (__cdecl *write)(Writer*,const void*,unsigned int,unsigned int*,unsigned int);};
struct Base{void FUN_00a5d7b0(Stream*);};struct Property:Base{
void* unk00;unsigned int unk04,unk08,unk0c,unk10,unk14;unsigned short mode;unsigned int flags,mask;
void FUN_00a6f740(Stream*);
};
void Property::FUN_00a6f740(Stream* stream){
FUN_00a5d7b0(stream);
unsigned int size=2; Writer* __restrict w=stream->writer();
w->bytesWritten+=w->write(w,&mode,2,&size,1);
size=4;w=stream->writer();w->bytesWritten+=w->write(w,&flags,4,&size,1);
size=4;w=stream->writer();w->bytesWritten+=w->write(w,&mask,4,&size,1);
}