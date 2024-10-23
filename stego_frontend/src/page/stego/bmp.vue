<template>
    <div class="sys-page">
        <app-title title="算法简介"></app-title>
        <div class="page-content">
            <app-notes>
                <p>读取图像：读取图像数据。将图像转换为 YUV 颜色空间。处理图像的透明通道（如果存在）。</p>
                <p>初始化分块索引：计算可以嵌入水印的块的数量，以备嵌入过程使用。</p>
                <p>嵌入水印：使用离散小波变换（DWT）和离散余弦变换（DCT）在图像的频域中嵌入水印。通过奇异值分解（SVD）调整 DCT 系数来隐藏水印信息。</p>
                <p>加速进程：利用多进程池加速水印嵌入过程。</p>
                <p>提取水印：使用 DWT 和 DCT 转换从图像中提取水印信息。通过 SVD 分解恢复隐藏的水印。</p>
            </app-notes>
            <app-section title="bmp图像嵌入">
                <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>bmp图像嵌入只支持上传bmp图像作为载体，txt文本文件存放隐写内容，输出为一个zip压缩文件，其中bmp图像为嵌入隐藏信息之后的图像，txt文件存放嵌入内容大小</p>
                    <p>在载体为1920*1080的条件下，嵌入大小为4023B。嵌入率为0.016 bpp</p>
                </div>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>载体图像</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".bmp"
                        :file-list="fileList1"
                        :on-success="handleSuccessBMP"
                        :on-remove="handleRemoveBMP"
                        multiple
                        :limit="1">
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    </el-upload>
                  </el-col>
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>隐藏内容</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".txt"
                        :file-list="fileList2"
                        :on-success="handleSuccessTXT"
                        :on-remove="handleRemoveTXT"
                        multiple
                        :limit="1">
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    </el-upload>
                  </el-col>
                </el-row>
                <div>
                    <el-row :gutter="20">
                    <el-col :span="8">
                      &nbsp;
                    </el-col>
                    <el-col :span="8">
                      <el-button type="primary" round
                                style="display: flex;justify-content: center;align-items: center;width: 70%;"
                                @click="embed"
                      >开始嵌入</el-button>
                    </el-col>
                    <el-col :span="8">
                      &nbsp;
                    </el-col>
                  </el-row>
                </div>
            </app-section>
  
  
  
            <app-section title="bmp图像提取">
              <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>bmp图像提取只支持上传bmp图像进行提取，同时需要输入该图片嵌入的信息大小</p>
                </div>
                <el-row :gutter="20">
                  <el-col :span="9">
                    <div class="sys-article">
                        <p><strong>待提取图像</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".bmp"
                        :file-list="fileList3"
                        :on-success="handleSuccessBMP2"
                        :on-remove="handleRemoveBMP2"
                        multiple
                        :limit="1">
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    </el-upload>
                  </el-col>
                  <el-col :span="5">
                    <div class="sys-article">
                        <p><strong>嵌入大小</strong></p>
                    </div>
                    <el-input
                      type="number"
                      placeholder="请输入嵌入大小"
                      v-model="embedLen">
                    </el-input>
                  </el-col>
                  <el-col :span="1">
                    &nbsp;
                  </el-col>
                  <el-col :span="9">
                    <div class="sys-article">
                        <p><strong>提取内容</strong></p>
                    </div>
                    <el-input
                      type="textarea"
                      :rows="6"
                      placeholder="请输入内容"
                      v-model="textarea"
                      readonly>
                    </el-input>
                  </el-col>
                </el-row>
                <div>
                    <el-row :gutter="20">
                    <el-col :span="8">
                      &nbsp;
                    </el-col>
                    <el-col :span="8">
                      <el-button type="primary" round
                                style="display: flex;justify-content: center;align-items: center;width: 70%;"
                                @click="extract"
                      >开始提取</el-button>
                    </el-col>
                    <el-col :span="8">
                      &nbsp;
                    </el-col>
                  </el-row>
                </div>
            </app-section>
        </div>
    </div>
  </template>
  
  <style>
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
  
  
  </style>
  
  
  <script>
  import axios from '@/util/ajax'
  import { mapState } from 'vuex'
  
  
  export default {
    computed: {
          ...mapState({
            userId: state => state.user.uid,
            username: state => state.user.name,
            user: state => state.user
          })
      },
    data() {
  
        return {
          name: 'bmp',
          textarea: '',
          filelist1: [],
          filelist2: [],
          filelist3: [],
          fileNameBMP: null,
          fileNameTXT: null,
          fileNameBMP2: null,
          embedLen: 0
      };
    },
    methods: {
      handleSuccessBMP2(response, file, fileList){
        console.log(response.filename)
        this.fileNameBMP2 = response.filename
      },
      handleRemoveBMP2(file, fileList) {
        this.fileNameBMP2 = null;
      },
      handleRemoveBMP(file, fileList) {
        this.fileNameBMP = null;
      },
      handleRemoveTXT(file, fileList) {
        this.fileNameTXT = null;
      },
      handleSuccessBMP(response, file, fileList){
        console.log(response.filename)
        this.fileNameBMP = response.filename
      },
      handleSuccessTXT(response, file, fileList){
        console.log(response.filename)
        this.fileNameTXT = response.filename
      },
      embed(){
        console.log(this.fileNameBMP)
        console.log(this.fileNameTXT)
  
        // 检查fileJPG是否为null
        if (this.fileNameBMP === null) {
            alert("请先上传载体图像");
            return; // 退出函数，不再执行后续代码
        }
  
        // 检查fileTXT是否为null
        if (this.fileNameTXT === null) {
            alert("请先上传隐藏信息");
            return; // 退出函数，不再执行后续代码
        }
  
        var that = this;
  
        this.loadingInstance  = this.starLoading();
  
  
        // 使用axios
        // 使用axios发送POST请求
        axios.post('/api/embedBMP', {
          fileNameBMP: that.fileNameBMP, // 你的请求参数
          fileNameTXT: that.fileNameTXT,
          userId: that.userId
        }, {
          responseType: 'blob' // 指定响应类型为blob
        })
        .then(response => {
  
          // 使用FileReader读取Blob对象
          const reader = new FileReader();
          reader.onload = (e) => {
            try {
              const resData = JSON.parse(e.target.result); // 尝试解析为JSON
              console.log('JSON解析成功1:', resData);
  
              this.$notify.error({
                title: '错误',
                message: resData.message
              });
  
  
            } catch (error) {
              console.error('JSON解析失败:', error);
  
              console.log(response)
              const url = window.URL.createObjectURL(new Blob([response]));
              const link = document.createElement('a');
              link.href = url;
              link.setAttribute('download', 'stegoBMP.zip'); // 指定下载的文件名
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
            } finally {
              this.$nextTick(() => {
                // 在 nextTick 之后关闭 loading
                this.loadingInstance.closeLoading();
              });
            }
          };
          reader.readAsText(response); // 读取Blob内容为文本
  
          this.$nextTick(() => {
          // 在 nextTick 之后关闭 loading
            this.loadingInstance.closeLoading();
          })
          })
          .catch(error => {
          console.error('There was an error!', error);
  
          this.$nextTick(() => {
          // 在 nextTick 之后关闭 loading
            this.loadingInstance.closeLoading();
          })
  
          });
  
  
  
      },
  
      extract() {
  
        // 检查fileJPG是否为null
        if (this.fileNameBMP2 === null) {
          alert("请先上传隐写图像");
          return; // 退出函数，不再执行后续代码
        }
  
        this.$set(this, 'textarea', "");
  
        this.loadingInstance = this.starLoading();
  
        console.log(this.embedLen)

        axios.post('/api/extractBMP', {
          fileNameBMP: this.fileNameBMP2,
          embedLen: this.embedLen,
          userId: this.userId
        }, {
          responseType: 'blob' // 确保响应类型为blob
        })
        .then(response => {
          // 使用FileReader读取Blob对象
          const reader = new FileReader();
          reader.onload = (e) => {
            try {
              const resData = JSON.parse(e.target.result); // 尝试解析为JSON
              console.log('JSON解析成功1:', resData);
  
              this.$notify.error({
                title: '错误',
                message: resData.message
              });
  
  
            } catch (error) {
              console.error('JSON解析失败:', error);
  
              // 将内容设置到textarea
              this.$set(this, 'textarea', e.target.result);
              console.log(e.target.result);
  
              // 创建一个可以下载的链接
              const url = window.URL.createObjectURL(new Blob([response]));
              const link = document.createElement('a');
              link.href = url;
              link.setAttribute('download', 'output.txt'); // 指定下载的文件名
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
              window.URL.revokeObjectURL(url); // 释放对象URL
            } finally {
              this.$nextTick(() => {
                // 在 nextTick 之后关闭 loading
                this.loadingInstance.closeLoading();
              });
            }
          };
          reader.readAsText(response); // 读取Blob内容为文本
        })
        .catch(error => {
          console.error('出现错误！', error);
          this.$nextTick(() => {
            // 在 nextTick 之后关闭 loading
            this.loadingInstance.closeLoading();
          });
        });
      },

  
      starLoading() {
        // 创建一个 loading 实例并赋值给 loading 变量
        let loading = this.$loading({
            text: "加载中", // 设置 loading 文本为 "加载中"
            spinner: "el-icon-loading", // 使用 Element UI 提供的加载图标
            background: "rgba(0, 0, 0, 0.7)", // 设置 loading 遮罩层背景色为半透明黑色
            target: document.querySelector("body"), // 将 loading 遮罩层挂载到页面 body 元素上
        });
        // 返回一个包含关闭 loading 遮罩层方法的对象
        return {
            // 方法用于关闭 loading 遮罩层
            closeLoading: () => {
                loading.close(); // 调用 loading 实例的 close 方法关闭遮罩层
            }
        };
      },
  
  
  
  
  
    }
  }
  </script>
  
  