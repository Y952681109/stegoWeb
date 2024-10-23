#ifndef __MI_WATER_H__
#define __MI_WATER_H__

#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
 
/* choose between declaration (GLOBAL undefined)
 * and definition (GLOBAL defined)
 * GLOBAL is defined in exactly one file mpeg2dec.c)
 */

#ifndef GLOBAL
#define EXTERN extern
#else
#define EXTERN
#endif

///////////////////////////////////////////////
//自己添加
struct  mi2In_file{
//内存操作
  void* InfileBuf;
  int InfileBufLen;
  int InfileBufPos;
////////////////////////////////////
};
struct  mi2Out_file{
//内存操作
  void* OutfileBuf;
  int OutfileBufLen;
  int OutfileBufPos;
////////////////////////////////////
};

EXTERN void mi2MemReadInit(void* Buffer,int Len);
EXTERN int mi2MemRead(void* Buffer,int size);
EXTERN void mi2MemWriteInit(void* Buffer,int Len);
EXTERN int mi2MemWrite(void* Buffer,int size);
EXTERN int mi2MemReadSeek(int offset);
EXTERN int mi2MemWriteSeek(int offset);
EXTERN void mi2MemCopyAll();
EXTERN void mi2MemCopyLeave();

//////////////////////////////////////////////
EXTERN void mi2FinishEmdMark(unsigned char *w,unsigned  char wlen);unsigned  long mi2FinishExtMark(unsigned char *w);

EXTERN unsigned  long mi2FinishExtMark(unsigned char *w);
////////////////////////////////////////////////////

#endif