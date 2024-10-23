#ifndef ERRORDEF_H
#define ERRORDEF_H

/*==============================================================================*/
/*Copyright: Information Security Center, Beijing University of Post and Telecom*/
/*author: yang cheng                                                            */
/*date: 2003.11                                                                 */
/*module: errordef.h                                                            */
/*==============================================================================*/

/*define */
#define NORMAL				0
/*define errors for embedding watermark*/
#define	ERR_EMD_MSGMAXLEN	1	/*message too long*/
#define	ERR_EMD_MSGZEROLEN	2	/*message is empty*/
#define ERR_EMD_COVTYPE		3	/*cover type wrong*/
#define	ERR_EMD_COVDATA		4	/*cover data wrong*/
#define ERR_EMD_MEMLOW		5	/*memery overflow*/
#define ERR_EMD_COVLEN		6	/*cover too small to hide message*/
#define ERR_EMD_PARAWRONG	7	/*parameter is wrong*/
#define ERR_EMD_REEMBED		8	/*already has a same watermark in the cover*/
#define	ERR_EMD_UNKNOWN		255	

/*define errors for extracting watermark*/
#define ERR_EXT_NOMSG		1	/*no message*/
#define	ERR_EXT_COVTYPE		2	/*cover type wrong*/
#define	ERR_EXT_COVDATA		3	/*cover data wrong*/
#define ERR_EXT_MEMLOW		4	/*memery overflow*/
#define ERR_EXT_PARAWRONG	5	/*parameter is wrong*/
#define	ERR_EXT_UNKNOWN		255

/*define operation type*/
#define DRM_EMBED			1
#define DRM_DISTILL		2

#endif

