#include "mi_water.h"
#include "memory.h"
 
struct  miIn_file miInfile;
struct  miOut_file miOutfile;
////////////////////////////////////
void miMemReadInit(void* Buffer,int Len)
{
	miInfile.InfileBuf=Buffer;
	miInfile.InfileBufLen=Len;
	miInfile.InfileBufPos=0; 
}

void miMemFeedback(char * * Buffer)
{
	(*Buffer)=(char *)(miInfile.InfileBuf)+miInfile.InfileBufPos;
}

int miMemRead(void* Buffer,int size)
{
	int RealSize;
	if((miInfile.InfileBufLen)>=(miInfile.InfileBufPos+size))
	{
		memcpy(Buffer,(void*)((char*)(miInfile.InfileBuf)+(miInfile.InfileBufPos)),size);
		(miInfile.InfileBufPos)+=size;
		return size;
	}
	else
	{
   		RealSize=miInfile.InfileBufLen-miInfile.InfileBufPos;
		memcpy(Buffer,(void*)((char*)(miInfile.InfileBuf)+(miInfile.InfileBufPos)),RealSize);
		miInfile.InfileBufPos+=RealSize;
		return RealSize;
	}
}

void miMemWriteInit(void* Buffer,int Len)
{
	miOutfile.OutfileBuf=Buffer;
	miOutfile.OutfileBufLen=Len;
	miOutfile.OutfileBufPos=0; 
}

int miMemWrite(void* Buffer,int size)
{
	int RealSize;
	if(miOutfile.OutfileBufLen>=(miOutfile.OutfileBufPos+size))
	{
		memcpy((void*)((char*)miOutfile.OutfileBuf+miOutfile.OutfileBufPos),Buffer,size);
		miOutfile.OutfileBufPos+=size;
		return size;
	}
	else
	{
	   	RealSize=miOutfile.OutfileBufLen-miOutfile.OutfileBufPos;
	    memcpy((void*)((char*)(miOutfile.OutfileBuf)+miOutfile.OutfileBufPos),Buffer,RealSize);
		miOutfile.OutfileBufPos+=RealSize;
		return RealSize;
	}
}

int miMemReadSeek(int offset)
{
	int pos=(miInfile.InfileBufPos)+offset;
	if((pos<(miInfile.InfileBufLen))  && (pos>=0))
	{
		miInfile.InfileBufPos=pos;
		return  0;
	}
	else
		return -1;
}

int miMemWriteSeek(int offset)
{
	int pos=(miOutfile.OutfileBufPos)+offset;
	if((pos<(miOutfile.OutfileBufLen))  && (pos>=0))
	{
		miOutfile.OutfileBufPos=pos;
		return  0;
	}
	else
	    return -1;
}

void miMemCopyAll()
{
	memcpy((void*)(miOutfile.OutfileBuf),
	   (void*)(miInfile.InfileBuf),
	   miInfile.InfileBufLen);  
}