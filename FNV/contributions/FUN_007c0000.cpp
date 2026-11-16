struct BSStringTChar {char* data;unsigned short length,capacity;~BSStringTChar();const char* FUN_00559450();};
struct Time {float FUN_00867da0();BSStringTChar FUN_00867970();const char* FUN_00867f10();};extern Time DAT_011de7b8;
struct Setting {const char* FUN_00403df0();};extern Setting DAT_011d24fc,DAT_011d27f0;
int __cdecl sprintf_s(char*,unsigned,const char*,...);
struct Tile {void FUN_00a01350(int,const char*,bool);};
struct Menu {int unk00,unk04,unk08,unk0C,unk10,unk14,unk18,unk1C,unk20,unk24,unk28,unk2C,unk30;Tile* tile;void FUN_007c0000();};
void Menu::FUN_007c0000()
{
 char text[260];int hour;
 {float time=DAT_011de7b8.FUN_00867da0();
  hour=(int)time;
  {int minute=(int)((time-hour)*60.0);
   if(time>=0.0 && time<1.0)hour=12;
   else if(time>=13.0)hour-=12;
   sprintf_s(text,260,"%s, %s, %d:%02d %s",DAT_011de7b8.FUN_00867f10(),DAT_011de7b8.FUN_00867970().FUN_00559450(),hour,minute,time<12.0?DAT_011d24fc.FUN_00403df0():DAT_011d27f0.FUN_00403df0());
  }
 }
 tile->FUN_00a01350(0xfc4,text,true);
}
