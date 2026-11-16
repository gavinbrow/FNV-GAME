struct LinkedIndexArray { int** entries; int count; void FUN_00d280e0(); };
void LinkedIndexArray::FUN_00d280e0(){
int* values=*entries; int* current=*entries; int* end=current+count;while(current!=end){if(*current>=0){while(values[*current]>=0){*current=values[*current];values=*entries;}}++current;}
}
