<template>
    <div class="sys-page">
        <app-title title="算法简介"></app-title>
        <div class="page-content">
            <app-notes>
                <p>读取WMA文件：使用音频处理工具FFmpeg将WMA格式的音频文件转换为无损的WAV格式。</p>
                <p>载入音频数据：从WAV文件中读取音频数据，通常这些数据是未压缩的音频波形样本。</p>
                <p>选择嵌入位置：确定秘密信息嵌入的位置，选择对听觉影响较小的样本部分，如LSB。</p>
                <p>编码秘密信息：将秘密信息编码为二进制序列，准备嵌入到音频样本中。</p>
                <p>嵌入信息：在WAV格式的音频样本的LSB中嵌入秘密信息。</p>
            </app-notes>
            <app-section title="wma音频嵌入">
                <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>wma音频嵌入只支持上传wma音频作为载体，txt文本文件存放信息。返回一个zip压缩文件，其中wma与wav文件都是进行加密后的音频</p>
                    <p>载体大小为5M的条件下，可以嵌入0.84MB信息。嵌入率为16.9%</p>
                </div>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>载体音频</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".wma"
                        :file-list="fileList1"
                        :on-success="handleSuccessWMA"
                        :on-remove="handleRemoveWMA"
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
  
  
  
            <app-section title="wma音频提取">
              <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>wma音频提取只支持上传隐写后的wav格式音频进行内容提取</p>
                </div>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>待提取音频</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".wav"
                        :file-list="fileList3"
                        :on-success="handleSuccessWMA2"
                        :on-remove="handleRemoveWMA2"
                        multiple
                        :limit="1">
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    </el-upload>
                  </el-col>
                  <el-col :span="12">
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
          name: 'wma',
          textarea: '',
          filelist1: [],
          filelist2: [],
          filelist3: [],
          fileNameWMA: null,
          fileNameTXT: null,
          fileNameWMA2: null,
      };
    },
    methods: {
      handleSuccessWMA2(response, file, fileList){
        console.log(response.filename)
        this.fileNameWMA2 = response.filename
      },
      handleRemoveWMA2(file, fileList) {
        this.fileNameWMA2 = null;
      },
      handleRemoveWMA(file, fileList) {
        this.fileNameWMA = null;
      },
      handleRemoveTXT(file, fileList) {
        this.fileNameTXT = null;
      },
      handleSuccessWMA(response, file, fileList){
        console.log(response.filename)
        this.fileNameWMA = response.filename
      },
      handleSuccessTXT(response, file, fileList){
        console.log(response.filename)
        this.fileNameTXT = response.filename
      },
      embed(){
        console.log(this.fileNameWMA)
        console.log(this.fileNameTXT)
  
        // 检查fileJPG是否为null
        if (this.fileNameWMA === null) {
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
        axios.post('/api/embedWMA', {
          fileNameWMA: that.fileNameWMA, // 你的请求参数
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
              link.setAttribute('download', 'stegoWMA.zip'); // 指定下载的文件名
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
        if (this.fileNameWMA2 === null) {
          alert("请先上传隐写音频");
          return; // 退出函数，不再执行后续代码
        }
  
        this.$set(this, 'textarea', "");
  
        this.loadingInstance = this.starLoading();
  
        axios.post('/api/extractWMA', {
          fileNameWAV: this.fileNameWMA2,
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
  
  