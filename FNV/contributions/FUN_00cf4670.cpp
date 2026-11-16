struct PacketStream {
    int metadata, bytesWritten, reserved;
    typedef int (__cdecl *Fn)(PacketStream*, const void*, int, int*, int);
    Fn write;
};
struct SerializedObject { int base00,base04,base08,base0C,base10,word14,word18;void __thiscall FUN_00cf4670(int source); };
extern "C" void __cdecl FUN_00d86160(int,SerializedObject*);
void SerializedObject::FUN_00cf4670(int source) {
int saved=source;FUN_00d86160(saved,this);
PacketStream *__restrict stream=*reinterpret_cast<PacketStream**>(saved+0x250);source=4;stream->bytesWritten+=stream->write(stream,&word14,4,&source,1);stream=*reinterpret_cast<PacketStream**>(saved+0x250);source=4;stream->bytesWritten+=stream->write(stream,&word18,4,&source,1);
}