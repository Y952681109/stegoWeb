#define GLOBAL
#include "mi_water.h"
#include "midwater.h"
#include "errordef.h"
 
#include "stdio.h"
#include "stdlib.h"

//������ϢΪ
//����(һ�ӽ�),ˮӡͷ("@@"),ˮӡ
//������8x,9x,ax,bx,cx���¼�����������ֽڵĺ���ֽ�
////////////////////////////////////////////////////////

//-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-//ˮӡǶ���㷨1
int MIDEmdWater(void * pmsg, unsigned short msglen, 
				void * psrc, unsigned long srclen, 
				void * pdest, unsigned long * pdestlen)
{
//===========================================//�������
	unsigned char * w;//ˮӡ
	unsigned char *pwlenhigh,*pwlenlow;
	unsigned char w1=0;//ˮӡ1��ͷ��@@���������з��ϵ��ֽ���
	unsigned char wlen,//ˮӡ����
		beforetemp,temp,wlentemp,track1,track2,head1,head2,head3,head4,
		flag=0,//0��ʾҪǶ��ˮӡ���ȣ�1��ʾҪǶ��ˮӡ����
		half=0;//0��ʾǶ���4λ��1��ʾǶ���4λ
	unsigned int i,t,track,//�켣�������
		cishu=0;//�ظ�Ƕ�����
	//unsigned int k;
	unsigned long head,j,count;
	//char c;
	int a,a1,a2;//��¼����������ֵ

	unsigned char c1=0,c2=0;//��¼Ƕ���־��##��
	unsigned char wlen2=0;

//===========================================//������
	if((msglen<=0) || (msglen>30))
	{
		if(msglen==0)//ˮӡ����Ϊ0
			return(ERR_EMD_MSGZEROLEN);
		if(msglen<0)//ˮӡ����С��0����������
			return(ERR_EMD_PARAWRONG);
		if(msglen>30)//ˮӡ���ȹ���
			return(ERR_EMD_MSGMAXLEN);
	}
	if(srclen<=0)//���峤��С��0����������
	{
		return(ERR_EMD_PARAWRONG);
	}

//===========================================//׼��ˮӡ������
	wlen=msglen+2;//ˮӡͷ("@@"),ˮӡ
	w=(unsigned char *)malloc(wlen);
	if(w==NULL)
	{
		return(ERR_EMD_MEMLOW);
	}
//	strcpy((char *)w,"@@");
	w[0]=w[1]=0x40;
	memcpy(w+2,pmsg,msglen);//w�д洢�ľ��Ǽ���ˮӡͷ��ˮӡ
	if((*pdestlen)<srclen)//������ڴ治��
	{
		free(w);
		return(ERR_EMD_MEMLOW);
	}

	(*pdestlen)=srclen;
  	miMemReadInit(psrc,srclen);
 	miMemWriteInit(pdest,*pdestlen);
 	miMemCopyAll();//��ԭʼ�����pcover����pnewcover
	count=0;
	pwlenlow=pwlenhigh=NULL;
	wlentemp=0;

//===========================================//����ļ���ʽ	
	if(count==srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	miMemRead(&temp,1);//�ļ���ʽ����
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
	if(a!=0)//��6���ֽ�Ҳû��������˵���ļ���ʽ����
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
	if(a<2)//��2���ֽ�Ҳû��������˵���ļ���ʽ����
	{
		free((void*)w);
		return(ERR_EMD_COVTYPE);
	}
	miMemWriteSeek(2);
	track=track1*256+track2;//�켣��ĸ���

	if((count+1)>=srclen)
	{
		free((void*)w);
		return(ERR_EMD_COVDATA);
	}
	a=miMemReadSeek(2);
	count+=2;
	if(a!=0)//��2���ֽ�Ҳû��������˵���ļ���ʽ����
	{
		free((void*)w);
		return(ERR_EMD_COVTYPE);
	}
	miMemWriteSeek(2);

//===========================================//Ƕ��ˮӡ
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
		miMemRead(&temp,1);//�ļ���ʽ����
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
		miMemRead(&temp,1);//�ļ���ʽ����
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
		miMemRead(&temp,1);//�ļ���ʽ����
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
		head=head*256+head4;//head��¼�켣�鳤��

		j=0;
		while(i<wlen && j<head-4)//һ�������Ĺ켣�鿪ʼ
		{
			if(w1==4)//�Ѿ�Ƕ��ˮӡ1��
			{
				(*pwlenlow)=(*pwlenlow) & 0xf0;//��ԭˮӡ����
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

			if(j<head-4 && (temp & 0x80)==0)//�ǲ����������λΪ0��˵�����ӳ٣�������һ���ֽ�Ӧ��������
			{
				beforetemp=temp;

				if(count==srclen)
				{
					free((void*)w);
					return(ERR_EMD_COVDATA);
				}
				miMemRead(&temp,1);//��������
				miMemWriteSeek(1);
				count++;
				j++;

				if(temp==0xf0 || temp==0xf2)//f0,f2����������
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
				if(temp==0xf3)//f3��һ������
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
				if(temp==0xff)//ff��������ֽڸ�������
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
				if(temp>=0xc0 && temp<=0xcf)//cx��һ������
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
					
					if(flag==0)//Ƕ��ˮӡ����
					{
						if(half==0)//Ƕ���4λ
						{
							miMemFeedback((char **)(&pwlenlow));
							wlentemp=(temp & 0x0f) | wlentemp;
							temp=temp & 0xf0;
							temp=temp | (wlen & 0x0f);
						}
						else//Ƕ���4λ
						{
							miMemFeedback((char **)(&pwlenhigh));
							wlentemp=((temp & 0x0f)<<4) | wlentemp;
							temp=temp & 0xf0;
							temp=temp | ((wlen & 0xf0)>>4);
						}
						if(half==1)
							flag=1;
					}
					else//Ƕ��ˮӡ
					{
						if(half==0)//Ƕ���4λ
						{
							if((i==0 || i==1) && cishu==1)//����Ƿ��Ѿ�Ƕ��ˮӡ1��
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
						else//Ƕ���4λ
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
						if(i==wlen)//ˮӡ�Ѿ�����Ƕ����һ����
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

//-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-//ˮӡ��ȡ�㷨1
int MIDExtWater(void * psrc, unsigned long srclen, 
				void * pmsg, unsigned short * pmsglen)
{
//===========================================//�������
	unsigned char* w;//ˮӡ+head
	unsigned char	wlen,//ˮӡ����
		beforetemp,temp,wlentemp=0,head1,head2,head3,head4,track1,track2,
		flag=0,//0��ʾҪ��ȡˮӡ���ȣ�1��ʾҪ��ȡˮӡ����
		half=0,//0��ʾ��ȡ��4λ��1��ʾ��ȡ��4λ
		situ;//��ȡˮӡʱ���Ƿ��γ����������ֽ�
	unsigned int i,k,t,
		track;//�켣�������
	unsigned int countcom=0;//��������Ƕ��ˮӡ��ָ��ĸ���
	unsigned long head,j,count,jj;
	int a,a1,a2;

	unsigned char c1=0,c2=0;//��¼Ƕ���־��##��
	unsigned char wlen2=0;

//===========================================//������
	if(srclen<10)
	{
		(*pmsglen)=0;
		return(ERR_EXT_PARAWRONG);
	}

//===========================================//׼������
	wlen=100;//������Ϊһ����ֵ
	w=(unsigned char *)malloc(wlen);
	if(w==NULL)
	{
		(*pmsglen)=0;
		return(ERR_EXT_MEMLOW);
	}
	miMemReadInit(psrc,srclen);
	count=0;
//===========================================//����ļ���ʽ
	if(count==srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	miMemRead(&temp,1);//�ļ���ʽ����
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
	if(a!=0)//��6���ֽ�Ҳû��������˵���ļ���ʽ����
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
	if(a<2)//��2���ֽ�Ҳû��������˵���ļ���ʽ����
	{
		(*pmsglen)=0;
		free((void*)w);
		return(ERR_EXT_COVTYPE);
	}
	track=track1*256+track2;//�켣�����
	if((count+1)>=srclen)
	{
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_COVDATA);
	}
	miMemReadSeek(2);
	count+=2;
//===========================================//��ȡˮӡ
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
		miMemRead(&temp,1);//�ļ���ʽ����
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
		miMemRead(&temp,1);//�ļ���ʽ����
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
		miMemRead(&temp,1);//�ļ���ʽ����
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
		miMemRead(&temp,1);//�ļ���ʽ����
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
		head=head*256+head4;//head��¼�켣�鳤��

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
			if(j<head-4 && (temp & 0x80)==0)//�ǲ����������λΪ0��˵�����ӳ٣�������һ���ֽ�Ӧ��������
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

				if(temp==0xf0 || temp==0xf2)//f0,f2����������
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
				if(temp==0xf3)//f3��һ������
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
				if(temp==0xff)//ff��������ֽڸ�������
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
				if(temp>=0xc0 && temp<=0xcf)//cx��һ������
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
					
					if(half==0)//��ȡ��4λ
						w[i]=temp & 0x0f;
					else//��ȡ��4λ
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

	//���ܵ�ˮӡ�Ѿ�����w�У����ڶ�w���д���
	j=0;
	flag=1;
	situ=1;
	while(j<(i-1) && flag==1)//i��w��Ԫ�صĸ���
	{
		if(w[j]==0x40 && w[j+1]==0x40)
			flag=0;
		j++;
	}
	if(flag==1)//w��û���ҵ�ˮӡͷ��@@��
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
	if(flag==0)//�кܴ���ܴ���ˮӡ
	{
		j--;//j��w�е�һ�γ���ˮӡͷ��@@�����Ǹ��ֽڵ�λ��
		if(situ==1)//ԭ��һ���ֽڵ�ˮӡ�����ڻ���һ���ֽ�
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
				if(flag==0)//�ҵ��˵ڶ���ˮӡͷ
				{
					jj--;//jj��w�еڶ��γ���ˮӡͷ��@@�����Ǹ��ֽڵ�λ��
					wlen=w[jj-1];
				}
				else//������ֻ��һ��ˮӡ������ˮӡ�ǲ������ģ�Ҳ����˵������Ϊû��ˮӡ
				{
					(*pmsglen)=0;
					free(w);
					return(ERR_EXT_NOMSG);
				}
			}
			if(wlen>32 || wlen<=2) //���Ȳ���
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
			if((unsigned int)(wlen+1)>i)//������ֻ��һ��ˮӡ������ˮӡ�ǲ������ģ�Ҳ����˵������Ϊû��ˮӡ
			{
				(*pmsglen)=0;
				free(w);
				return(ERR_EXT_NOMSG);
			}
			for(k=j+2;k<(j+wlen) && k<i;k++)
				((char *)pmsg)[k-j-2]=w[k];
			if(k<(j+wlen))//ˮӡû�ж��꣬��Ҫ����ȥ�������ˮӡ
			{
				for(k=j-2;k>=i-wlen-1;k--)
					((char *)pmsg)[k-j+wlen-1]=w[k];
			}
			(*pmsglen)=wlen-2;
			free(w);
			return(NORMAL);
		}
		else//situ==0ԭ��һ���ֽڵ�ˮӡ�����������ֽ���
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
				if(flag==0)//�ҵ��˵ڶ���ˮӡͷ
				{
					jj--;//jj��w�еڶ��γ���ˮӡͷ��@@�����Ǹ��ֽڵ�λ��
					wlen=((w[jj] & 0x0f)<<4) | ((w[jj-1] & 0xf0)>>4);
				}
				else//������ֻ��һ��ˮӡ������ˮӡ�ǲ������ģ�Ҳ����˵������Ϊû��ˮӡ
				{
					(*pmsglen)=0;
					free(w);
					return(ERR_EXT_NOMSG);
				}
			}
			if(wlen>32 || wlen<=2) //���Ȳ���
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
			if((unsigned int)(wlen+1+1)>i)//������ֻ��һ��ˮӡ������ˮӡ�ǲ������ģ�Ҳ����˵������Ϊû��ˮӡ
			{
				(*pmsglen)=0;
				free(w);
				return(ERR_EXT_NOMSG);
			}
			for(k=j+2;k<(j+wlen-1) && k<(i-1);k++)
				((char *)pmsg)[k-j-2]=((w[j] & 0xf0)>>4) | ((w[j+1] & 0x0f)<<4);
			if(k<(j+wlen-1))//ˮӡû�ж��꣬��Ҫ����ȥ�������ˮӡ
			{
				for(k=j-1;k>=i-wlen-1;k--)
					((char *)pmsg)[k-j+wlen-2]=((w[k] & 0x0f)<<4) | ((w[k-1] & 0xf0)>>4);
			}
			(*pmsglen)=wlen-2;
			free(w);
			return(NORMAL);
		}
	}
	else//������ˮӡ
	{
        printf("don't have watermark\n");
		(*pmsglen)=0;
		free(w);
		return(ERR_EXT_NOMSG);
	}
}
