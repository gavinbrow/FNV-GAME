struct EventSource {
    void __thiscall FUN_0040f6e0();
};
union PacketValue {
    unsigned int bits;
    unsigned char byte;
};
struct EventMessage {
    unsigned int code;
    EventSource* source;
    union {
        struct {
            PacketValue first;
            PacketValue second;
            PacketValue third;
        } arguments;
        unsigned char serializedArguments[24];
    } payload;
};
struct Receiver {
    void __thiscall FUN_0087d160(EventMessage* message);
    void __thiscall FUN_0087b300(EventSource* source, unsigned char first,
                                unsigned char second, unsigned char third);
};
void Receiver::FUN_0087b300(EventSource* source, unsigned char first,
                             unsigned char second, unsigned char third)
{
    EventMessage message;
    message.code = 49;
    message.source = source;
    message.payload.arguments.first.byte = first;
    message.payload.arguments.second.byte = second;
    message.payload.arguments.third.byte = third;
    source->FUN_0040f6e0();
    FUN_0087d160(&message);
}