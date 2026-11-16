#include "h_7cbbb4b7bd5f.h"

struct FUN_0048cee0_class
{
	virtual void Slot00();
	virtual void Slot01();
	virtual void Slot02();
	virtual void Slot03();
	virtual void Slot04();
	virtual int Slot05();
	int __thiscall FUN_0048cee0();
};

struct FUN_0045a5e0_class
{
	void __thiscall FUN_0045a5e0(int value);
};

extern FUN_0045a5e0_class* DAT_011c3b3c;

struct FUN_0050d600_shell
{
	int unk00;
	int unk04;
	int unk08;
	int unk0c;
	int unk10;
	int unk14;
	int unk18;
	int unk1c;
	int unk20;
	int unk24;
	int unk28;
	int unk2c;
	int unk30;
	int unk34;
	int unk38;
	FUN_0048cee0_class unk3c;

	void __thiscall FUN_0050d600(int value);
};

void __thiscall FUN_0050d600_shell::FUN_0050d600(int value)
{
	if (unk3c.FUN_0048cee0())
	{
		DAT_011c3b3c->FUN_0045a5e0(unk3c.Slot05());
	}
}