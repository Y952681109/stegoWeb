#ifndef __MIDWATER_H__
#define __MIDWATER_H__

int MIDEmdWater(void * pmsg, unsigned short msglen,
				void * psrc, unsigned long srclen,
				void * pdest, unsigned long * pdestlen);

int MIDExtWater(void * psrc, unsigned long srclen,
				void * pmsg, unsigned short * pmsglen);
 
int MIDEmdWater2nd(void * pmsg, unsigned short msglen,
				   void * psrc, unsigned long srclen,
				   void * pdest, unsigned long * pdestlen);

int MIDExtWater2nd(void * psrc, unsigned long srclen,
					 void * pmsg, unsigned short * pmsglen);

#endif