#ifndef __MI_WATER_H__
#define __MI_WATER_H__

#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
 

#ifndef GLOBAL
#define EXTERN extern
#else
#define EXTERN
#endif

///////////////////////////////////////////////
//自己添加
struct  miIn_file{
//内存操作
  void* InfileBuf;
  int InfileBufLen;
  int InfileBufPos;
////////////////////////////////////
};
struct  miOut_file{
//内存操作
  void* OutfileBuf;
  int OutfileBufLen;
  int OutfileBufPos;
////////////////////////////////////
};

EXTERN void miMemReadInit(void* Buffer,int Len);
EXTERN void miMemFeedback(char * * Buffer);
EXTERN int miMemRead(void* Buffer,int size);
EXTERN void miMemWriteInit(void* Buffer,int Len);
EXTERN int miMemWrite(void* Buffer,int size);
EXTERN int miMemReadSeek(int offset);
EXTERN int miMemWriteSeek(int offset);
EXTERN void miMemCopyAll();


#endif