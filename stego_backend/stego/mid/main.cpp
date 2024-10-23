#include <stdio.h>
#include "midwater.h"
#include <string.h>
#include <stdlib.h>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>
// #include "aes_api.h"
// #include <jni.h>


void OnDistill(char* output, char* outputtxt,char* key="1234567890abcdef")
{
 char *m_filePath=output;

 FILE *inFile;
 unsigned long inFileLen;
 char *pInFile;
 unsigned short wmInfoLen = strlen("111122222hello");
 char wmInfo[1024] = "0";
 char fileNameSuffix[256];
char *fileName;
 char wav[4] = "wav";
char gif[4] = "gif";
 char jpg[4] = "jpg";
char mpeg[5] = "mpeg";
 char mpg[4] = "MPG";
 unsigned short filePathLen;
 
 inFile = fopen(m_filePath, "rb"); //replace "m_filePath1" with the real path
 if (!inFile) 
 {
 printf("Could not open file for reading\n");
return;
 }
 
fseek(inFile, 0, SEEK_END);
inFileLen = ftell(inFile);
 rewind(inFile);

 pInFile = (char *)malloc(inFileLen);
 fread(pInFile, 1, inFileLen, inFile);

 strcpy(fileNameSuffix, strrchr(m_filePath, '.')); //replace "m_filePath1" with the real path fileName = fileNameSuffix + 1;
 int result = MIDExtWater(pInFile, inFileLen, &wmInfo, &wmInfoLen);
 printf("%s\n", wmInfo);

// aes_decrypt(wmInfo,outputtxt,key);
char * file_txt = outputtxt;
 FILE * txt_file = fopen(file_txt, "wb");
 fwrite(wmInfo,sizeof(char),strlen(wmInfo),txt_file);

free(pInFile);
fclose(inFile);
fclose(txt_file);
}

void enbed(char *original, char* output, char* plaintxt, char* key="1234567890abcdef")
{
    char *m_filePath=original; //载体mid文件
    char *m_wmInfo; //嵌入信息
	

    // std::string encryptedString = aes_encypt(plaintxt,key);
    char * file_txt = plaintxt;
    FILE * txt_file = fopen(file_txt, "rb");
    fseek(txt_file, 0, SEEK_END);
    int txtFileLen = ftell(txt_file);
    fseek(txt_file, 0, SEEK_SET);
    m_wmInfo = (char *)malloc(sizeof(char)*(txtFileLen+1));
    fread(m_wmInfo,sizeof(char),txtFileLen,txt_file);
     m_wmInfo[txtFileLen]='\0';
    printf("m_wmInfo = %s\n",m_wmInfo);
    // std::vector<char> buffer(encryptedString.begin(), encryptedString.end());
    // buffer.push_back('\0');  // 确保字符串以 null 结尾

    // char* m_wmInfo = &buffer[0];  // 获取字符数组的指针
    

    unsigned char *wmInfo = (unsigned char *)m_wmInfo;
    unsigned short wmInfoLen = (unsigned short)strlen(m_wmInfo);

    unsigned long inFileLen;
    FILE *inFile;
    inFile = fopen(m_filePath, "rb");
    fseek(inFile, 0, SEEK_END);
    inFileLen = ftell(inFile);
    fseek(inFile, 0, SEEK_SET);
    unsigned long *pInFile = (unsigned long *)malloc(inFileLen);
    fread(pInFile, 1, inFileLen, inFile);
    unsigned long *pOutFile = (unsigned long *)malloc(2 * inFileLen);
    unsigned long outFileLen = inFileLen;
    unsigned long *pOutFileLen = &outFileLen;

    //获取载体文件格式，即后缀
    unsigned short filePathLen = strlen(m_filePath);
    char *filePath = m_filePath;
    while (*(filePath + filePathLen) != '.') {
        filePathLen--;
    }
    unsigned short fileNameSuffixLen = strlen(m_filePath) - filePathLen;
    char *fileName = (char *)malloc(fileNameSuffixLen);
    for (int i = 0; i < fileNameSuffixLen; i++) {
        *(fileName + i) = *(filePath + filePathLen + 1 + i);
    }
	
	MIDEmdWater(wmInfo, wmInfoLen, pInFile, inFileLen, pOutFile, pOutFileLen);
 	//char fileToSave[20] = output;
            FILE *outFile;
            outFile = fopen(output, "wb");
            fwrite(pOutFile, 1, *pOutFileLen, outFile);
            fclose(outFile);
            printf("The watermark is embed successfully!\n");
  free(fileName);
  free(pInFile);
  free(pOutFile);
  fclose(inFile);

}
// jstring Java_com_example_myapplication_MainActivity_midencode( JNIEnv* env,jobject thiz ,jstring originalfilePath,jstring outputfilePath,jstring plainfilePath)
// {

//         // 获取文件路径
//         const char *originalpath = (*env)->GetStringUTFChars(env, originalfilePath, NULL);
//         const char *outputpath = (*env)->GetStringUTFChars(env, outputfilePath, NULL);
//         const char *plainpath = (*env)->GetStringUTFChars(env, plainfilePath, NULL);


//    enbed(originalpath,outputpath,plainpath);

// 	return (*(*env)).NewStringUTF(env, "success encode");

// }
// jstring Java_com_example_myapplication_MainActivity_middecode( JNIEnv* env,jobject thiz ,jstring outputfilePath,jstring outputplainfilePath)
// {

//         // 获取文件路径
//         const char *outputpath = (*env)->GetStringUTFChars(env, outputfilePath, NULL);
//         const char *plainpath = (*env)->GetStringUTFChars(env, outputplainfilePath, NULL);


//    OnDistill(outputpath,plainpath);

// 	return (*(*env)).NewStringUTF(env, "success decode");

// }

void en(){
    std::cout<<"请依次输入载体mid文件名、输出载密mid文件名、载密文本："<<std::endl;
    std::string origin;
    std::string output;
    std::string secret;
    std::cin>>origin>>output>>secret;
    std::vector<char> buffer(origin.begin(), origin.end());
    buffer.push_back('\0');  // 确保字符串以 null 结尾
    char* m_origin = &buffer[0];  // 获取字符数组的指针

    std::vector<char> buffer1(output.begin(), output.end());
    buffer1.push_back('\0');  // 确保字符串以 null 结尾
    char* m_output = &buffer1[0];  // 获取字符数组的指针

    std::vector<char> buffer2(secret.begin(), secret.end());
    buffer2.push_back('\0');  // 确保字符串以 null 结尾
    char* m_secret = &buffer2[0];  // 获取字符数组的指针

    // enbed("origin.mid","output.mid","1.txt");
    enbed(m_origin,m_output,m_secret);
}

void de(){
    std::cout<<"请依次输入载密mid文件名、输出文本文件名："<<std::endl;
    std::string output;
    std::string secret;
    std::cin>>output>>secret;

    std::vector<char> buffer1(output.begin(), output.end());
    buffer1.push_back('\0');  // 确保字符串以 null 结尾
    char* m_output = &buffer1[0];  // 获取字符数组的指针

    std::vector<char> buffer2(secret.begin(), secret.end());
    buffer2.push_back('\0');  // 确保字符串以 null 结尾
    char* m_secret = &buffer2[0];  // 获取字符数组的指针
    // OnDistill("output.mid","out.txt");
    OnDistill(m_output,m_secret);
}
int main(){
    
    // en();

    
    de();

    return 0;
}