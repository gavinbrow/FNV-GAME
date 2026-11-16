void __cdecl FUN_00e31650(int count,float** array,float first,float last){
float* values=*array;*values=first;values[count]=last;
int i=1;
if(count-1>=4){
 int limit=count-3; int j=3;
 do{
values[i]=(float)i/(float)count*(last-first)+first;
values[i+1]=(float)(j-1)/(float)count*(last-first)+first;
values[i+2]=(float)j/(float)count*(last-first)+first;
values[i+3]=(float)(i+3)/(float)count*(last-first)+first;
 i+=4;j+=4;
 }while(i<limit);
 }
 if(i<count){
 float* output=values+i;
 do{*output=(float)i/(float)count*(last-first)+first;++output;++i;}while(i<count);
 }
}