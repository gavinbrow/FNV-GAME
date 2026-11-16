// Uses insights from unverified 2026-10-23 contributor attempt.
extern int DAT_0109ff64;
struct SSE_Node : NiExtraData {
 void* m_vtbl;unsigned int unk04,unk08,unk0C,unk10;int unk14;
 static void* operator new(unsigned int size) {return BSFadeNode::operator new(size);}
 SSE_Node() throw() { FUN_00a7b2e0();m_vtbl=&DAT_0109ff64;unk10=0;unk0C=0;unk14=-1;}
};
struct SSE_Owner: NiSwitchStringExtraData {
 SSE_Node* FUN_00a938d0(unsigned int);void FUN_00a937a0(SSE_Node*,unsigned int);
};
SSE_Node* SSE_Owner::FUN_00a938d0(unsigned int arg) {
 SSE_Node* obj=new SSE_Node;
 FUN_00a937a0(obj,arg);
 return obj;
}