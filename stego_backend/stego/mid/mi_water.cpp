#define GLOBAL
#include "mi_water.h"
#include "midwater.h"
#include "errordef.h"
 
#include "stdio.h"
#include "stdlib.h"

//隐藏信息为
//长度(一子节),水印头("@@"),水印
//隐藏在8x,9x,ax,bx,cx的事件命令后三个字节的后半字节
////////////////////////////////////////////////////////

//-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-//水印嵌入算法1
int MIDEmdWater(void * pmsg, unsigned short msglen, 
				void * psrc, unsigned long srclen, 
				void * pdest, unsigned long * pdestlen)
{
//===========================================//定义变量
	unsigned char * w;//水印
	unsigned char *pwlenhigh,*pwlenlow;
	unsigned char w1=0;//水印1的头“@@”在载体中符合的字节数
	unsigned char wlen,//水印长度
		beforetemp,temp,wlentemp,track1,track2,head1,head2,head3,head4,
		flag=0,//0表示要嵌入水印长度；1表示要嵌入水印内容
		half=0;//0表示嵌入低4位；1表示嵌入高4位
	unsigned int i,t,track,//轨迹块的数量
		cishu=0;//重复嵌入次数
	//unsigned int k;
	unsigned long head,j,count;
	//char c;
	int a,a1,a2;//记录各函数返回值

	unsigned char c1=0,c2=0;//记录嵌入标志“##”
	unsigned char wlen2=0;

//===========================================//检查参数
	if((msglen<=0) || (msglen>30))
	{
		if(msglen==0)//水印长度为0
			return(ERR_EMD_MSGZEROLEN);
		if(msglen<0)//水印长度小于0，参数错误
			return(ERR_EMD_PARAWRONG);
		if(msglen>30)//水印长度过长
			return(ERR_EMD_MSGMAXLEN);
	}
	if(srclen<=0)//载体长度小于0，参数错误
	{
		return(ERR_EMD_PARAWRONG);
	}

//===========================================//准备水印和载体
	wlen=msglen+2;//水印头("@@"),水印
	w=(unsigned char *)malloc(wlen);
	if(w==NULL)
	{
		return(ERR_EMD_MEMLOW);
	}
//	strcpy((char *)w,"@@");
	w[0]=w[1]=0x40;
	memcpy(w+2,pmsg,msglen);//w中存储的就是加入水印头的水印
	if((*pdestlen)<srclen)//分配的内存不够
	{
		free(w);
		return(ERR_EMD_MEMLOW);
	}

	(*pdestlen)=srclen;
  	miMemReadInit(psrc,srclen);
 	miMemWriteInit(pdest,*pdestlen);
 	miMemCopyAll();//将原始载体从pcover拷到pnewcover
	count=0;
	pwlenlow=pwlenhigh=NULL;
	wlentemp=0;

//===========================================//检查文件格式	
	if(count==srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	miMemRead(&temp,1);//文件格式错误
	miMemWriteSeek(1);
	count++;
	if(temp!=0x4d)
	{
		free((void*)w);
		return(ERR_EMD_COVTYPE);
	}
	if(count==srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	miMemRead(&temp,1);
	miMemWriteSeek(1);
	count++;
	if(temp!=0x54)
	{
		free((void*)w);
		return(ERR_EMD_COVTYPE);
	}
	if(count==srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	miMemRead(&temp,1);
	miMemWriteSeek(1);
	count++;
	if(temp!=0x68)
	{
		free((void*)w);
		return(ERR_EMD_COVTYPE);
	}
	if(count==srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	miMemRead(&temp,1);
	miMemWriteSeek(1);
	count++;
	if(temp!=0x64)
	{
		free((void*)w);
		return(ERR_EMD_COVTYPE);
	}
	
	if((count+5)>=srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	a=miMemReadSeek(6);
	count+=6;
	if(a!=0)//连6个字节也没读出来，说明文件格式错误
	{
		free((void*)w);
		return(ERR_EMD_COVTYPE);
	}
	miMemWriteSeek(6);

	if(count==srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	a1=miMemRead(&track1,1);
	count++;
	if(count==srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	a2=miMemRead(&track2,1);
	count++;
	a=a1+a2;
	if(a<2)//连2个字节也没读出来，说明文件格式错误
	{
		free((void*)w);
		return(ERR_EMD_COVTYPE);
	}
	miMemWriteSeek(2);
	track=track1*256+track2;//轨迹块的个数

	if((count+1)>=srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	a=miMemReadSeek(2);
	count+=2;
	if(a!=0)//连2个字节也没读出来，说明文件格式错误
	{
		free((void*)w);
		return(ERR_EMD_COVTYPE);
	}
	miMemWriteSeek(2);

//===========================================//嵌入水印
	i=0;
	t=0;
	cishu=1;
	while(i<wlen && t<track)
	{
		if(count==srclen)
		{
			free((void*)w);
			return(ERR_EMD_COVDATA);
		}
		miMemRead(&temp,1);//文件格式错误
		miMemWriteSeek(1);
		count++;
		if(temp!=0x4d)
		{
			free((void*)w);
			return(ERR_EMD_COVTYPE);
		}
		if(count==srclen)
		{
			free((void*)w);
			return(ERR_EMD_COVDATA);
		}
		miMemRead(&temp,1);
		miMemWriteSeek(1);
		count++;
		if(temp!=0x54)
		{
			free((void*)w);
			return(ERR_EMD_COVTYPE);
		}
		if(count==srclen)
		{
			free((void*)w);
			return(ERR_EMD_COVDATA);
		}
		miMemRead(&temp,1);//文件格式错误
		miMemWriteSeek(1);
		count++;
		if(temp!=0x72)
		{
			free((void*)w);
			return(ERR_EMD_COVTYPE);
		}
		if(count==srclen)
		{
			free((void*)w);
			return(ERR_EMD_COVDATA);
		}
		miMemRead(&temp,1);//文件格式错误
		miMemWriteSeek(1);
		count++;
		if(temp!=0x6b)
		{
			free((void*)w);
			return(ERR_EMD_COVTYPE);
		}

		if(count==srclen)
		{
			free((void*)w);
			return(ERR_EMD_COVDATA);
		}
		miMemRead(&head1,1);
		count++;
		if(count==srclen)
		{
			free((void*)w);
			return(ERR_EMD_COVDATA);
		}
		miMemRead(&head2,1);
		count++;
		if(count==srclen)
		{
			free((void*)w);
			return(ERR_EMD_COVDATA);
		}
		miMemRead(&head3,1);
		count++;
		if(count==srclen)
		{
			free((void*)w);
			return(ERR_EMD_COVDATA);
		}
		miMemRead(&head4,1);
		count++;
		miMemWriteSeek(4);
		head=head1*256+head2;
		head=head*256+head3;
		head=head*256+head4;//head记录轨迹块长度

		j=0;
		while(i<wlen && j<head-4)//一个正常的轨迹块开始
		{
			if(w1==4)//已经嵌入水印1了
			{
				(*pwlenlow)=(*pwlenlow) & 0xf0;//还原水印长度
				(*pwlenlow)=(*pwlenlow) | (wlentemp & 0x0f);
				(*pwlenhigh)=(*pwlenhigh) & 0xf0;
				(*pwlenhigh)=(*pwlenhigh) | ((wlentemp & 0xf0)>>4);
				free((void*)w);
				return(ERR_EMD_REEMBED);
			}
			if(count==srclen)
			{
				free((void*)w);
				return(ERR_EMD_COVDATA);
			}
			miMemRead(&temp,1);
			miMemWriteSeek(1);
			count++;
			j++;

			if(j<head-4 && (temp & 0x80)==0)//是参数而且最高位为0，说明是延迟，而且下一个字节应该是命令
			{
				beforetemp=temp;

				if(count==srclen)
				{
					free((void*)w);
					return(ERR_EMD_COVDATA);
				}
				miMemRead(&temp,1);//读入命令
				miMemWriteSeek(1);
				count++;
				j++;

				if(temp==0xf0 || temp==0xf2)//f0,f2带两个参数
				{
					if((count+1)>=srclen)
					{
						free((void*)w);
						return(ERR_EMD_COVDATA);
					}
					miMemReadSeek(2);
					miMemWriteSeek(2);
					count+=2;
					j+=2;
				}
				if(temp==0xf3)//f3带一个参数
				{
					if(count==srclen)
					{
						free((void*)w);
						return(ERR_EMD_COVDATA);
					}
					miMemReadSeek(1);
					miMemWriteSeek(1);
					count++;
					j++;
				}
				if(temp==0xff)//ff后面带的字节个数不定
				{
					if(count==srclen)
					{
						free((void*)w);
						return(ERR_EMD_COVDATA);
					}
					miMemReadSeek(1);
					miMemWriteSeek(1);
					count++;
					j+=1;
					if(count==srclen)
					{
						free((void*)w);
						return(ERR_EMD_COVDATA);
					}
					miMemRead(&beforetemp,1);
					miMemWriteSeek(1);
					count++;
					j++;
					if((count+beforetemp-1)>=srclen)
					{
						free((void*)w);
						return(ERR_EMD_COVDATA);
					}
					miMemReadSeek(beforetemp);
					miMemWriteSeek(beforetemp);
					count+=beforetemp;
					j+=beforetemp;
				}
				if(temp>=0xc0 && temp<=0xcf)//cx带一个参数
				{
					if(count==srclen)
					{
						free((void*)w);
						return(ERR_EMD_COVDATA);
					}
					miMemReadSeek(1);
					miMemWriteSeek(1);
					count++;
					j++;
				}

				if(temp>=0x80 && temp<=0xbf)//8x,9x,ax,bx
				{
					if(count==srclen)
					{
						free((void*)w);
						return(ERR_EMD_COVDATA);
					}
					miMemReadSeek(1);
					miMemWriteSeek(1);
					count++;
					j++;

					if(count==srclen)
					{
						free((void*)w);
						return(ERR_EMD_COVDATA);
					}
					miMemRead(&temp,1);
					count++;
					j++;
					
					if(flag==0)//嵌入水印长度
					{
						if(half==0)//嵌入低4位
						{
							miMemFeedback((char **)(&pwlenlow));
							wlentemp=(temp & 0x0f) | wlentemp;
							temp=temp & 0xf0;
							temp=temp | (wlen & 0x0f);
						}
						else//嵌入高4位
						{
							miMemFeedback((char **)(&pwlenhigh));
							wlentemp=((temp & 0x0f)<<4) | wlentemp;
							temp=temp & 0xf0;
							temp=temp | ((wlen & 0xf0)>>4);
						}
						if(half==1)
							flag=1;
					}
					else//嵌入水印
					{
						if(half==0)//嵌入低4位
						{
							if((i==0 || i==1) && cishu==1)//检查是否已经嵌过水印1了
								if((temp & 0x0f)==0x00)
								{
									w1++;
									half=(half+1)%2;
									miMemWriteSeek(1);
									continue;
								}
							temp=temp & 0xf0;
							temp=temp | (w[i] & 0x0f);
						}
						else//嵌入高4位
						{
							if((i==0 || i==1) && cishu==1)
								if((temp & 0x0f)==0x04)
								{
									w1++;
									i++;
									half=(half+1)%2;
									miMemWriteSeek(1);
									continue;
								}
							temp=temp & 0xf0;
							temp=temp | ((w[i] & 0xf0)>>4);
						}
						if(half==1)
							i++;
						if(i==wlen)//水印已经完整嵌入完一次了
						{
							cishu++;
							i=0;
							flag=0;
						}
					}

					half=(half+1)%2;
					miMemWrite(&temp,1);
				}//8x,9x,ax,bx
			}
		}//while(i<wlen && j<head-4)
		if((count+(head-j)-1)>=srclen)
		{
			free((void*)w);
			return(ERR_EMD_COVDATA);
		}
		miMemReadSeek(head-j);
		miMemWriteSeek(head-j);
		count+=(head-j);
		t++;
	}//while(i<wlen && t<track)
	 free((void*)w);
	if(i<wlen && cishu==1)
		return(ERR_EMD_COVLEN);
	else
		return(NORMAL);
}

//-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-//水印提取算法1
int MIDExtWater(void * psrc, unsigned long srclen, 
				void * pmsg, unsigned short * pmsglen)
{
//===========================================//定义变量
	unsigned char* w;//水印+head
	unsigned char	wlen,//水印长度
		beforetemp,temp,wlentemp=0,head1,head2,head3,head4,track1,track2,
		flag=0,//0表示要提取水印长度；1表示要提取水印内容
		half=0,//0表示提取低4位；1表示提取高4位
		situ;//提取水印时，是否形成了完整的字节
	unsigned int i,k,t,
		track;//轨迹块的数量
	unsigned int countcom=0;//读过的能嵌有水印的指令的个数
	unsigned long head,j,count,jj;
	int a,a1,a2;

	unsigned char c1=0,c2=0;//记录嵌入标志“##”
	unsigned char wlen2=0;

//===========================================//检查参数
	if(srclen<10)
	{
		(*pmsglen)=0;
		return(ERR_EXT_PARAWRONG);
	}

//===========================================//准备变量
	wlen=100;//先设置为一个大值
	w=(unsigned char *)malloc(wlen);
	if(w==NULL)
	{
		(*pmsglen)=0;
		return(ERR_EXT_MEMLOW);
	}
	miMemReadInit(psrc,srclen);
	count=0;
//===========================================//检查文件格式
	if(count==srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	miMemRead(&temp,1);//文件格式错误
	count++;
	if(temp!=0x4d)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVTYPE);
	}
	if(count==srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	miMemRead(&temp,1);
	count++;
	if(temp!=0x54)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVTYPE);
	}
	if(count==srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	miMemRead(&temp,1);
	count++;
	if(temp!=0x68)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVTYPE);
	}
	if(count==srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	miMemRead(&temp,1);
	count++;
	if(temp!=0x64)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVTYPE);
	}
	
	if((count+5)>=srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	a=miMemReadSeek(6);
	count+=6;
	if(a!=0)//连6个字节也没读出来，说明文件格式错误
	{
		(*pmsglen)=0;
		free((void*)w);
		return(ERR_EXT_COVTYPE);
	}

	if(count==srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	a1=miMemRead(&track1,1);
	count++;
	if(count==srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	a2=miMemRead(&track2,1);
	count++;
	a=a1+a2;
	if(a<2)//连2个字节也没读出来，说明文件格式错误
	{
		(*pmsglen)=0;
		free((void*)w);
		return(ERR_EXT_COVTYPE);
	}
	track=track1*256+track2;//轨迹块个数
	if((count+1)>=srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	miMemReadSeek(2);
	count+=2;
//===========================================//提取水印
	i=0;
	t=0;
	while(i<wlen && t<track)
	{
		if(count==srclen)
		{
			(*pmsglen)=0;
			free(w);
			return(ERR_EXT_COVDATA);
		}
		miMemRead(&temp,1);//文件格式错误
		count++;
		if(temp!=0x4d)
		{
			(*pmsglen)=0;
			free((void*)w);
			return(ERR_EXT_COVTYPE);
		}
		if(count==srclen)
		{
			(*pmsglen)=0;
			free(w);
			return(ERR_EXT_COVDATA);
		}
		miMemRead(&temp,1);//文件格式错误
		count++;
		if(temp!=0x54)
		{
			(*pmsglen)=0;
			free((void*)w);
			return(ERR_EXT_COVTYPE);
		}
		if(count==srclen)
		{
			(*pmsglen)=0;
			free(w);
			return(ERR_EXT_COVDATA);
		}
		miMemRead(&temp,1);//文件格式错误
		count++;
		if(temp!=0x72)
		{
			(*pmsglen)=0;
			free((void*)w);
			return(ERR_EXT_COVTYPE);
		}
		if(count==srclen)
		{
			(*pmsglen)=0;
			free(w);
			return(ERR_EXT_COVDATA);
		}
		miMemRead(&temp,1);//文件格式错误
		count++;
		if(temp!=0x6b)
		{
			(*pmsglen)=0;
			free((void*)w);
			return(ERR_EXT_COVTYPE);
		}

		if(count==srclen)
		{
			(*pmsglen)=0;
			free(w);
			return(ERR_EXT_COVDATA);
		}
		miMemRead(&head1,1);
		count++;
		if(count==srclen)
		{
			(*pmsglen)=0;
			free(w);
			return(ERR_EXT_COVDATA);
		}
		miMemRead(&head2,1);
		count++;
		if(count==srclen)
		{
			(*pmsglen)=0;
			free(w);
			return(ERR_EXT_COVDATA);
		}
		miMemRead(&head3,1);
		count++;
		if(count==srclen)
		{
			(*pmsglen)=0;
			free(w);
			return(ERR_EXT_COVDATA);
		}
		miMemRead(&head4,1);
		count++;
		head=head1*256+head2;
		head=head*256+head3;
		head=head*256+head4;//head记录轨迹块长度

		j=0;
		while(i<wlen && j<head-4)
		{
			if(count==srclen)
			{
				(*pmsglen)=0;
				free(w);
				return(ERR_EXT_COVDATA);
			}
			miMemRead(&temp,1);
			count++;
			j++;
			if(j<head-4 && (temp & 0x80)==0)//是参数而且最高位为0，说明是延迟，而且下一个字节应该是命令
			{
				beforetemp=temp;
				if(count==srclen)
				{
					(*pmsglen)=0;
					free(w);
					return(ERR_EXT_COVDATA);
				}
				miMemRead(&temp,1);
				count++;
				j++;

				if(temp==0xf0 || temp==0xf2)//f0,f2带两个参数
				{
					if((count+1)>=srclen)
					{
						(*pmsglen)=0;
						free(w);
						return(ERR_EXT_COVDATA);
					}
					miMemReadSeek(2);
					count+=2;
					j+=2;
				}
				if(temp==0xf3)//f3带一个参数
				{
					if(count==srclen)
					{
						(*pmsglen)=0;
						free(w);
						return(ERR_EXT_COVDATA);
					}
					miMemReadSeek(1);
					count++;
					j++;
				}
				if(temp==0xff)//ff后面带的字节个数不定
				{
					if(count==srclen)
					{
						(*pmsglen)=0;
						free(w);
						return(ERR_EXT_COVDATA);
					}
					miMemReadSeek(1);
					miMemWriteSeek(1);
					count++;
					j+=1;
					if(count==srclen)
					{
						(*pmsglen)=0;
						free(w);
						return(ERR_EXT_COVDATA);
					}
					miMemRead(&beforetemp,1);
					miMemWriteSeek(1);
					count++;
					j++;
					if((count+beforetemp-1)>=srclen)
					{
						(*pmsglen)=0;
						free(w);
						return(ERR_EXT_COVDATA);
					}
					miMemReadSeek(beforetemp);
					miMemWriteSeek(beforetemp);
					count+=beforetemp;
					j+=beforetemp;
				}
				if(temp>=0xc0 && temp<=0xcf)//cx带一个参数
				{
					if(count==srclen)
					{
						(*pmsglen)=0;
						free(w);
						return(ERR_EXT_COVDATA);
					}
					miMemReadSeek(1);
					count++;
					j++;
				}

				if(temp>=0x80 && temp<=0xbf)//8x,9x,ax,bx
				{
					if(count==srclen)
					{
						(*pmsglen)=0;
						free(w);
						return(ERR_EXT_COVDATA);
					}
					miMemReadSeek(1);
					count++;
					j++;
					if(count==srclen)
					{
						(*pmsglen)=0;
						free(w);
						return(ERR_EXT_COVDATA);
					}
					miMemRead(&temp,1);
					count++;
					j++;
					temp=temp & 0x0f;
					
					if(half==0)//提取低4位
						w[i]=temp & 0x0f;
					else//提取高4位
						w[i]=((temp & 0x0f)<<4) | w[i];
					if(half==1)
						i++;
					half=(half+1)%2;
				}//8x,9x,ax,bx
			}
		}//while(i<wlen && j<head-4)
		if((count+(head-j)-1)>=srclen)
		{
			(*pmsglen)=0;
			free(w);
			return(ERR_EXT_COVDATA);
		}
		miMemReadSeek(head-j);
		count+=(head-j);
		t++;
	}

	//可能的水印已经读到w中，现在对w进行处理
	j=0;
	flag=1;
	situ=1;
	while(j<(i-1) && flag==1)//i是w中元素的个数
	{
		if(w[j]==0x40 && w[j+1]==0x40)
			flag=0;
		j++;
	}
	if(flag==1)//w中没有找到水印头“@@”
	{
		j=0;
		flag=1;
		situ=0;
		while(j<(i-2) && flag==1)
		{
			if((w[j] & 0xf0)==0 && w[j+1]==0x04 && (w[j+2] & 0x0f)==0x04)
				flag=0;
			j++;
		}
	}
	if(flag==0)//有很大可能存在水印
	{
		j--;//j是w中第一次出现水印头“@@”的那个字节的位置
		if(situ==1)//原来一个字节的水印，现在还是一个字节
		{
			if(j>=1)
			{
				wlen=w[j-1];
			}
			else
			{
				jj=2;
				flag=1;
				while(jj<(i-1) && flag==1)
				{
					if(w[jj]==0x40 && w[jj+1]==0x40)
						flag=0;
					jj++;
				}
				if(flag==0)//找到了第二个水印头
				{
					jj--;//jj是w中第二次出现水印头“@@”的那个字节的位置
					wlen=w[jj-1];
				}
				else//载体中只有一个水印，而且水印是不完整的，也就是说可以认为没有水印
				{
					(*pmsglen)=0;
					free(w);
					return(ERR_EXT_NOMSG);
				}
			}
			if(wlen>32 || wlen<=2) //长度不对
			{
				(*pmsglen)=0;
				free(w);
				return(ERR_EXT_UNKNOWN);
			}
			if((wlen-2)>(*pmsglen))
			{
				(*pmsglen)=0;
				free(w);
				return(ERR_EXT_MEMLOW);
			}
			if((unsigned int)(wlen+1)>i)//载体中只有一个水印，而且水印是不完整的，也就是说可以认为没有水印
			{
				(*pmsglen)=0;
				free(w);
				return(ERR_EXT_NOMSG);
			}
			for(k=j+2;k<(j+wlen) && k<i;k++)
				((char *)pmsg)[k-j-2]=w[k];
			if(k<(j+wlen))//水印没有读完，还要倒回去读后面的水印
			{
				for(k=j-2;k>=i-wlen-1;k--)
					((char *)pmsg)[k-j+wlen-1]=w[k];
			}
			(*pmsglen)=wlen-2;
			free(w);
			return(NORMAL);
		}
		else//situ==0原来一个字节的水印，被拆到两个字节中
		{
			if(j>=1)
				wlen=((w[j] & 0x0f)<<4) | ((w[j-1] & 0xf0)>>4);
			else
			{
				jj=0;
				flag=1;
				while(jj<(i-2) && flag==1)
				{
					if((w[jj] & 0xf0)==0 && w[jj+1]==0x04 && (w[jj+2] & 0x0f)==0x04)
						flag=0;
					jj++;
				}
				if(flag==0)//找到了第二个水印头
				{
					jj--;//jj是w中第二次出现水印头“@@”的那个字节的位置
					wlen=((w[jj] & 0x0f)<<4) | ((w[jj-1] & 0xf0)>>4);
				}
				else//载体中只有一个水印，而且水印是不完整的，也就是说可以认为没有水印
				{
					(*pmsglen)=0;
					free(w);
					return(ERR_EXT_NOMSG);
				}
			}
			if(wlen>32 || wlen<=2) //长度不对
			{
				(*pmsglen)=0;
				free(w);
				return(ERR_EXT_UNKNOWN);
			}
			if((wlen-2)>(*pmsglen))
			{
				(*pmsglen)=0;
				free(w);
				return(ERR_EXT_MEMLOW);
			}
			if((unsigned int)(wlen+1+1)>i)//载体中只有一个水印，而且水印是不完整的，也就是说可以认为没有水印
			{
				(*pmsglen)=0;
				free(w);
				return(ERR_EXT_NOMSG);
			}
			for(k=j+2;k<(j+wlen-1) && k<(i-1);k++)
				((char *)pmsg)[k-j-2]=((w[j] & 0xf0)>>4) | ((w[j+1] & 0x0f)<<4);
			if(k<(j+wlen-1))//水印没有读完，还要倒回去读后面的水印
			{
				for(k=j-1;k>=i-wlen-1;k--)
					((char *)pmsg)[k-j+wlen-2]=((w[k] & 0x0f)<<4) | ((w[k-1] & 0xf0)>>4);
			}
			(*pmsglen)=wlen-2;
			free(w);
			return(NORMAL);
		}
	}
	else//不存在水印
	{
        printf("don't have watermark\n");
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_NOMSG);
	}
}
