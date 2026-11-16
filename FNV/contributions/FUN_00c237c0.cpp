struct FNVStreamWriter{ void* owner;unsigned int writtenBytes;void* streamState;int(__cdecl*write)(FNVStreamWriter*,const void*,unsigned int,unsigned int*,int);};
struct FNVStreamArchive {};
struct FNVSubproperty{void FUN_00a69780(FNVStreamArchive*);};
struct FNVSerializer{void FUN_00c31950(FNVStreamArchive*);void FUN_00c237c0(FNVStreamArchive*);};
void FNVSerializer::FUN_00c237c0(FNVStreamArchive* stream) {
FUN_00c31950(stream);
typedef void (__thiscall* HeaderWriter)(FNVStreamArchive*,unsigned int);
HeaderWriter head=reinterpret_cast<HeaderWriter>((*reinterpret_cast<void***>(stream))[12]);
head(stream,*reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this)+0x18));
reinterpret_cast<FNVSubproperty*>(reinterpret_cast<char*>(this)+0x1c)->FUN_00a69780(stream);
FNVStreamWriter* __restrict writer;
unsigned int length;
length=4;writer=*reinterpret_cast<FNVStreamWriter**>(reinterpret_cast<char*>(stream)+0x250);
writer->writtenBytes+=writer->write(writer,reinterpret_cast<char*>(this)+0x28,4,reinterpret_cast<unsigned int*>(&length),1);
length=4;writer=*reinterpret_cast<FNVStreamWriter**>(reinterpret_cast<char*>(stream)+0x250);
writer->writtenBytes+=writer->write(writer,reinterpret_cast<char*>(this)+0x2c,4,reinterpret_cast<unsigned int*>(&length),1);
length=4;writer=*reinterpret_cast<FNVStreamWriter**>(reinterpret_cast<char*>(stream)+0x250);
writer->writtenBytes+=writer->write(writer,reinterpret_cast<char*>(this)+0x30,4,reinterpret_cast<unsigned int*>(&length),1);
length=4;writer=*reinterpret_cast<FNVStreamWriter**>(reinterpret_cast<char*>(stream)+0x250);
writer->writtenBytes+=writer->write(writer,reinterpret_cast<char*>(this)+0x34,4,reinterpret_cast<unsigned int*>(&length),1);
length=4;writer=*reinterpret_cast<FNVStreamWriter**>(reinterpret_cast<char*>(stream)+0x250);
writer->writtenBytes+=writer->write(writer,reinterpret_cast<char*>(this)+0x38,4,reinterpret_cast<unsigned int*>(&length),1);
length=1;writer=*reinterpret_cast<FNVStreamWriter**>(reinterpret_cast<char*>(stream)+0x250);
writer->writtenBytes+=writer->write(writer,reinterpret_cast<char*>(this)+0x3c,1,reinterpret_cast<unsigned int*>(&length),1);
}