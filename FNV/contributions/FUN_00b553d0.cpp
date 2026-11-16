#include "h_c2fd73dcb295.h"

struct FUN_00b553d0_PropertyLayout
{
	unsigned int unk00;
	unsigned int unk04;
	unsigned int unk08;
	unsigned int unk0c;
	unsigned int unk10;
	unsigned int unk14;
	unsigned int unk18;
	unsigned int unk1c;
	unsigned int unk20;
	unsigned int unk24;
	NiPoint3 value;
	unsigned int unk34;
	unsigned int unk38;
	unsigned int unk3c;
	unsigned int unk40;
	unsigned int count;
};

struct FUN_00b553d0_NodeLayout
{
	unsigned int unk00;
	unsigned int unk04;
	unsigned int unk08;
	unsigned int unk0c;
	unsigned int unk10;
	unsigned int unk14;
	unsigned int unk18;
	unsigned int unk1c;
	unsigned int unk20;
	unsigned int unk24;
	unsigned int unk28;
	unsigned int unk2c;
	unsigned int unk30;
	unsigned int unk34;
	unsigned int unk38;
	unsigned int unk3c;
	unsigned int unk40;
	unsigned int unk44;
	unsigned int unk48;
	unsigned int unk4c;
	unsigned int unk50;
	unsigned int unk54;
	unsigned int unk58;
	unsigned int unk5c;
	unsigned int unk60;
	unsigned int unk64;
	unsigned int unk68;
	unsigned int unk6c;
	unsigned int unk70;
	unsigned int unk74;
	unsigned int unk78;
	unsigned int unk7c;
	unsigned int unk80;
	unsigned int unk84;
	unsigned int unk88;
	unsigned int unk8c;
	unsigned int unk90;
	unsigned int unk94;
	unsigned int unk98;
	unsigned int unk9c;
	NiAVObject** children;
	unsigned short unkA4;
	unsigned short childCount;
};

void __cdecl FUN_00b553d0(NiGeometry* pObject, NiPoint3* pValue)
{
	if (pObject == 0)
		return;

	if (pObject->IsGeometry() != 0)
	{
		NiProperty* pFirst = pObject->GetProperty(2);
		NiProperty* pSecond = pObject->GetProperty(3);

		if (pFirst != 0 && pSecond != 0)
		{
			FUN_00b553d0_PropertyLayout* pFirstLayout =
				(FUN_00b553d0_PropertyLayout*)pFirst;
			FUN_00b553d0_PropertyLayout* pSecondLayout =
				(FUN_00b553d0_PropertyLayout*)pSecond;

			if ((pSecondLayout->unk20 & 0x20000000u) <= 0)
				return;

			pFirstLayout->value = *pValue;
			++pFirstLayout->count;
		}
		return;
	}

	NiNode* pNode = pObject->IsNode();
	if (pNode == 0)
		return;

	FUN_00b553d0_NodeLayout* pNodeLayout =
		(FUN_00b553d0_NodeLayout*)pNode;

	unsigned int count = pNodeLayout->childCount;
	for (unsigned int i = 0; i < count; ++i)
	{
		NiAVObject* pChild = pNodeLayout->children[i];
		if (pChild != 0)
			FUN_00b553d0((NiGeometry*)pChild, pValue);
	}
}