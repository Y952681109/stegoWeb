#include "mi2_water.h"
#include "memory.h"
 
struct  mi2In_file mi2Infile;
struct  mi2Out_file mi2Outfile;
////////////////////////////////////
void mi2MemReadInit(void* Buffer,int Len)
{
	mi2Infile.InfileBuf=Buffer;
	mi2Infile.InfileBufLen=Len;
	mi2Infile.InfileBufPos=0; 
}

int mi2MemRead(void* Buffer,int size)
{
	int RealSize;
	if(mi2Infile.InfileBufLen>=(mi2Infile.InfileBufPos+size))
	{
		memcpy(Buffer,(void*)((char*)(mi2Infile.InfileBuf)+mi2Infile.InfileBufPos),size);
		mi2Infile.InfileBufPos+=size;
		return size;
	}
	else
	{
   		RealSize=mi2Infile.InfileBufLen-mi2Infile.InfileBufPos;
		memcpy(Buffer,(void*)((char*)(mi2Infile.InfileBuf)+mi2Infile.InfileBufPos),RealSize);
		mi2Infile.InfileBufPos+=RealSize;
		return RealSize;
	}
}

void mi2MemWriteInit(void* Buffer,int Len)
{
	mi2Outfile.OutfileBuf=Buffer;
	mi2Outfile.OutfileBufLen=Len;
	mi2Outfile.OutfileBufPos=0; 
}

int mi2MemWrite(void* Buffer,int size)
{
	int RealSize;
	if(mi2Outfile.OutfileBufLen>=(mi2Outfile.OutfileBufPos+size))
	{
		memcpy((void*)((char*)mi2Outfile.OutfileBuf+mi2Outfile.OutfileBufPos),Buffer,size);
		mi2Outfile.OutfileBufPos+=size;
		return size;
	}
	else
	{
   		RealSize=mi2Outfile.OutfileBufLen-mi2Outfile.OutfileBufPos;
		memcpy((void*)((char*)(mi2Outfile.OutfileBuf)+mi2Outfile.OutfileBufPos),Buffer,RealSize);
		mi2Outfile.OutfileBufPos+=RealSize;
		return RealSize;
	}
}

int mi2MemReadSeek(int offset)
{
	int pos=mi2Infile.InfileBufPos+offset;
	if((pos<(mi2Infile.InfileBufLen))  && (pos>=0))
	{
		mi2Infile.InfileBufPos=pos;
		return  0;
	}
	else
	    return -1;
}

int mi2MemWriteSeek(int offset)
{
	int pos=mi2Outfile.OutfileBufPos+offset;
	if((pos<(mi2Outfile.OutfileBufLen))  && (pos>=0))
	{
		mi2Outfile.OutfileBufPos=pos;
		return  0;
	}
	else
	    return -1;
}

void mi2MemCopyAll()
{
	memcpy((void*)(mi2Outfile.OutfileBuf),
	   (void*)(mi2Infile.InfileBuf),
	   mi2Infile.InfileBufLen);  
}

void mi2MemCopyLeave()
{
	memcpy((void*)((char*)(mi2Outfile.OutfileBuf)+mi2Outfile.OutfileBufPos),
	   (void*)((char*)(mi2Infile.InfileBuf)+mi2Infile.InfileBufPos),
	   mi2Infile.InfileBufLen-mi2Infile.InfileBufPos);  
}