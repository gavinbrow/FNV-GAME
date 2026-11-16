#include "h_f943c85d47e7.h"
static inline NiNode* GetNext(NiTListItem<NiNode*>*& node){NiNode*& element=node->m_element;node=node->m_pkNext;return element;}
class FNVEffect:public NiDynamicEffect{public:bool __thiscall FUN_00a5a260(FNVEffect* other);bool __thiscall FUN_00a68d80(FNVEffect* other);};
bool __thiscall FNVEffect::FUN_00a68d80(FNVEffect* other){if(!FUN_00a5a260(other))return false;
if(m_kAffectedNodeList.m_kAllocator.m_uiCount!=other->m_kAffectedNodeList.m_kAllocator.m_uiCount)return false;
if(m_kAffectedNodeList.m_kAllocator.m_uiCount>0){NiTListItem<NiNode*>* left=m_kAffectedNodeList.m_pkHead;NiTListItem<NiNode*>* right=other->m_kAffectedNodeList.m_pkHead;
while(left){NiNode* a=GetNext(left);NiNode* b=GetNext(right);if(a && !b)return false;if(!a && b)return false;}}
if(m_kUnaffectedNodeList.m_kAllocator.m_uiCount!=other->m_kUnaffectedNodeList.m_kAllocator.m_uiCount)return false;
if(m_kUnaffectedNodeList.m_kAllocator.m_uiCount>0){NiTListItem<NiNode*>* left=m_kUnaffectedNodeList.m_pkHead;NiTListItem<NiNode*>* right=other->m_kUnaffectedNodeList.m_pkHead;
while(left){NiNode* a=GetNext(left);NiNode* b=GetNext(right);if(a && !b)return false;if(!a && b)return false;}}
return true;}