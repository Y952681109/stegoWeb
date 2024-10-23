<template>
    <div class="sys-page">
        <app-title title="算法简介"></app-title>
        <div class="page-content">
            <app-notes>
                <p>载体处理：使用 librosa.load 读取音频文件并将其转换为单通道16kHz采样率。</p>
                <p>信息处理：读取秘密文件并将其转换为二进制字符串，处理文件扩展名并添加到二进制字符串前。</p>
                <p>样本分割：根据分割长度和采样率计算每个分割的样本数，准备秘密信息并填充到32的倍数长度。</p>
                <p>信号编码：将二进制字符串转换为 NumPy 数组，使用 wavmark 库的模型对音频信号进行编码。</p>
                <p>嵌入信息：遍历音频信号，每次处理一定长度的音频，使用模型的 encode 方法将秘密信息嵌入音频中。</p>
                <p>音频合并：将编码后的音频信号片段与原始音频信号的其他部分合并，形成最终的输出音频。</p>
                <p>音频保存：保存包含嵌入秘密信息的音频信号为新的 WAV 文件。</p>
            </app-notes>
            <app-section title="wav音频嵌入">
                <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>wav音频嵌入只支持上传wav音频作为载体，txt文本文件存储秘密信息</p>
                    <p>载体大小为5M条件下可以嵌入665B信息。嵌入率为0.013%</p>
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
                        accept=".wav"
                        :file-list="fileList1"
                        :on-success="handleSuccessWAV"
                        :on-remove="handleRemoveWAV"
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
  
  
  
            <app-section title="wav音频提取">
              <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>wav音频提取只支持上传wav音频进行提取</p>
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
                        :on-success="handleSuccessWAV2"
                        :on-remove="handleRemoveWAV2"
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
          name: 'wavDL',
          textarea: '',
          filelist1: [],
          filelist2: [],
          filelist3: [],
          fileNameWAV: null,
          fileNameTXT: null,
          fileNameWAV2: null,
      };
    },
    methods: {
      handleSuccessWAV2(response, file, fileList){
        console.log(response.filename)
        this.fileNameWAV2 = response.filename
      },
      handleRemoveWAV2(file, fileList) {
        this.fileNameWAV2 = null;
      },
      handleRemoveWAV(file, fileList) {
        this.fileNameWAV = null;
      },
      handleRemoveTXT(file, fileList) {
        this.fileNameTXT = null;
      },
      handleSuccessWAV(response, file, fileList){
        console.log(response.filename)
        this.fileNameWAV = response.filename
      },
      handleSuccessTXT(response, file, fileList){
        console.log(response.filename)
        this.fileNameTXT = response.filename
      },
      embed(){
        console.log(this.fileNameWAV)
        console.log(this.fileNameTXT)
  
        // 检查fileJPG是否为null
        if (this.fileNameWAV === null) {
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
        axios.post('/api/embedWAVDL', {
          fileNameWAV: that.fileNameWAV, // 你的请求参数
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
              link.setAttribute('download', 'stegoWAV.wav'); // 指定下载的文件名
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
        if (this.fileNameWAV2 === null) {
          alert("请先上传隐写图像");
          return; // 退出函数，不再执行后续代码
        }
  
        this.$set(this, 'textarea', "");
  
        this.loadingInstance = this.starLoading();
  
        axios.post('/api/extractWAVDL', {
          fileNameWAV: this.fileNameWAV2,
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
  
  