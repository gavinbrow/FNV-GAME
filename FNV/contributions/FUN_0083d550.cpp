struct FUN_008579e0_shell {void FUN_008579e0(void*,unsigned int);};
extern FUN_008579e0_shell* g_TESSaveLoadGame;
void FUN_00403d30(void*,int,unsigned int);
struct BSStr {char* data;unsigned short length,capacity;bool Set(const char*,unsigned int);};
struct Record {BSStr first;unsigned int flags,value;BSStr second;void FUN_0083d550();};
void Record::FUN_0083d550() {
 unsigned char firstLength,secondLength;
 g_TESSaveLoadGame->FUN_008579e0(&firstLength,1);
 if(firstLength) {
  char firstBuffer[260];
  FUN_00403d30(firstBuffer,0,260);
  g_TESSaveLoadGame->FUN_008579e0(firstBuffer,firstLength);
  first.Set(firstBuffer,0);
 } else first.Set("",0);
 g_TESSaveLoadGame->FUN_008579e0(&secondLength,1);
 if(secondLength) {
  char secondBuffer[260];
  FUN_00403d30(secondBuffer,0,260);
  g_TESSaveLoadGame->FUN_008579e0(secondBuffer,secondLength);
  second.Set(secondBuffer,0);
 } else second.Set("",0);
 g_TESSaveLoadGame->FUN_008579e0(&flags,4);
 g_TESSaveLoadGame->FUN_008579e0(&value,4);
}
