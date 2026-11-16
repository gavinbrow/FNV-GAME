extern unsigned int DAT_011dd428;
extern unsigned int DAT_011dd448;
struct LoadBuffer : BGSLoadGameBuffer {
    void __thiscall FUN_00865e50(void*,unsigned int,unsigned int);
    void __thiscall FUN_00865e70(void*,unsigned int);
    unsigned int __thiscall FUN_00865f20();
    void __thiscall FUN_00865ff0(unsigned int,unsigned int);
    void __thiscall FUN_00865df0(unsigned int,unsigned int);
};
struct RadioForm {
    unsigned int __thiscall FUN_007af430();
};
void __cdecl FUN_008366e0(LoadBuffer* buffer)
{
    unsigned int secondID5;
    unsigned int receiverNode4;
    FalloutRadio::FORadioReceiver* formID;
    unsigned int formCount;
    BSSimpleList<FalloutRadio::FORadioReceiver*>* stationPosition4;
    unsigned int firstID2;
    unsigned int receiverCount;
    unsigned int stationCount;
    BSSimpleList<FalloutRadio::StationState*>* formNode2;
    FalloutRadio::StationState* receiverPosition;
    unsigned int station_2;
    unsigned int formPosition4;
    BSSimpleList<unsigned int>* stationNode;
    unsigned int receiver5;
    
    buffer->FUN_00865e50(&DAT_011dd428,4,0);
    buffer->FUN_00865e50(&DAT_011dd434,1,0);
    buffer->FUN_00865e70(&DAT_011dd448,0);
    
    firstID2=0;
    formCount=buffer->FUN_00865f20();
    stationPosition4=&DAT_011dd58c;
    while(stationPosition4) {
        formID=stationPosition4->GetItem();
        if(formID) {
            formID->InitLoadGame(buffer);
            ++firstID2;
        }
        stationPosition4=stationPosition4->GetNext();
    }
    buffer->FUN_00865ff0(firstID2,formCount);
    
    stationCount=0;
    receiverCount=buffer->FUN_00865f20();
    formNode2=&DAT_011dd554;
    while(formNode2) {
        receiverPosition=formNode2->GetItem();
        if(receiverPosition) {
            receiverPosition->InitLoadGame(buffer);
            ++stationCount;
        }
        formNode2=formNode2->GetNext();
    }
    buffer->FUN_00865ff0(stationCount,receiverCount);
    
    secondID5=0;
    if(DAT_011dd42c)
        secondID5=(*(RadioForm**)DAT_011dd42c)->FUN_007af430();
    buffer->FUN_00865df0(secondID5,0);
    receiverNode4=0;
    if(DAT_011dd430)
        receiverNode4=(*(RadioForm**)DAT_011dd430)->FUN_007af430();
    buffer->FUN_00865df0(receiverNode4,0);
    
    station_2=0;
    formPosition4=buffer->FUN_00865f20();
    stationNode=&DAT_011dd59c;
    while(stationNode) {
        receiver5=stationNode->GetItem();
        if(receiver5) {
            buffer->FUN_00865df0(receiver5,0);
            ++station_2;
        }
        stationNode=stationNode->GetNext();
    }
    buffer->FUN_00865ff0(station_2,formPosition4);
}
