<template>
    <div class="sys-page">
        <app-title title="算法简介"></app-title>
        <div class="page-content">
            <app-notes>
                <p>视频处理：读取原始视频文件，分离视频流和音频流。将视频流分解为单独的帧（图像序列）。</p>
                <p>音频信息处理：提取原始视频的音轨信息并保存，以便在合成视频时重新加入。</p>
                <p>帧差异性分析：分析连续帧之间的差异，确定嵌入信息的容量。视频帧之间的相似性较高，因此需要小心选择嵌入位置和量，以避免造成视频质量下降或产生可见的闪烁。</p>
                <p>深度学习模型：RivaGAN 使用一个基于深度学习的生成对抗网络（GAN），该网络包含两个独立的对抗网络，用于评估和优化视频质量与水印的鲁棒性。</p>
                <p>自定义嵌入机制：利用基于注意力的机制将自定义数据嵌入到视频帧中，这种机制允许算法在嵌入过程中关注视频的关键部分，以减少视觉失真。</p>
                <p>水印嵌入：在视频帧中嵌入信息，创建水印视频。嵌入的信息量受到限制，以避免视频质量下降或产生可见的闪烁。</p>
                <p>视频帧重建：将嵌入了水印信息的帧重新组合成视频流。</p>
                <p>视频合成：将处理过的视频流与原始音轨合并，生成最终的水印视频。</p>
            </app-notes>
            <app-section title="avi视频嵌入">
                <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>avi视频嵌入只支持上传avi视频作为载体，txt文本文件存放隐藏信息</p>
                    <p>最多支持嵌入4B信息</p>
                </div>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>载体视频</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".avi"
                        :file-list="fileList1"
                        :on-success="handleSuccessAVI"
                        :on-remove="handleRemoveAVI"
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
                    <el-col :span="6">
                        &nbsp;
                    </el-col>
                    <el-col :span="5">
                        <el-button type="primary" round
                                style="display: flex;justify-content: center;align-items: center;width: 70%;"
                                @click="embed(0)"
                        >开始嵌入(CPU)</el-button>
                    </el-col>
                    <el-col :span="2">
                        &nbsp;
                    </el-col>
                    <el-col :span="5">
                        <el-button type="primary" round
                                style="display: flex;justify-content: center;align-items: center;width: 70%;"
                                @click="embed(1)"
                        >开始嵌入(GPU)</el-button>
                    </el-col>
                    <el-col :span="6">
                        &nbsp;
                    </el-col>
                    </el-row>
                </div>
            </app-section>
  
  
  
            <app-section title="avi视频提取">
              <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>avi视频提取只支持上传avi视频进行提取</p>
                </div>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>待提取视频</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".avi"
                        :file-list="fileList3"
                        :on-success="handleSuccessAVI2"
                        :on-remove="handleRemoveAVI2"
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
                    <el-col :span="6">
                        &nbsp;
                    </el-col>
                    <el-col :span="5">
                        <el-button type="primary" round
                                style="display: flex;justify-content: center;align-items: center;width: 70%;"
                                @click="extract(0)"
                        >开始提取(CPU)</el-button>
                    </el-col>
                    <el-col :span="2">
                        &nbsp;
                    </el-col>
                    <el-col :span="5">
                        <el-button type="primary" round
                                style="display: flex;justify-content: center;align-items: center;width: 70%;"
                                @click="extract(1)"
                        >开始提取(GPU)</el-button>
                    </el-col>
                    <el-col :span="6">
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
          name: 'aviDL',
          textarea: '',
          filelist1: [],
          filelist2: [],
          filelist3: [],
          fileNameAVI: null,
          fileNameTXT: null,
          fileNameAVI2: null,
      };
    },
    methods: {
      handleSuccessAVI2(response, file, fileList){
        console.log(response.filename)
        this.fileNameAVI2 = response.filename
      },
      handleRemoveAVI2(file, fileList) {
        this.fileNameAVI2 = null;
      },
      handleRemoveAVI(file, fileList) {
        this.fileNameAVI = null;
      },
      handleRemoveTXT(file, fileList) {
        this.fileNameTXT = null;
      },
      handleSuccessAVI(response, file, fileList){
        console.log(response.filename)
        this.fileNameAVI = response.filename
      },
      handleSuccessTXT(response, file, fileList){
        console.log(response.filename)
        this.fileNameTXT = response.filename
      },
      embed(param){
        console.log(this.fileNameAVI)
        console.log(this.fileNameTXT)
        console.log(param)
        // 检查fileJPG是否为null
        if (this.fileNameAVI === null) {
            alert("请先上传载体视频");
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
        axios.post('/api/embedAVIDL', {
          fileNameAVI: that.fileNameAVI, // 你的请求参数
          fileNameTXT: that.fileNameTXT,
          method: param,
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
              link.setAttribute('download', 'stegoAVI.avi'); // 指定下载的文件名
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
  
      extract(param) {
  
        // 检查fileJPG是否为null
        if (this.fileNameAVI2 === null) {
          alert("请先上传隐写视频");
          return; // 退出函数，不再执行后续代码
        }
  
        this.$set(this, 'textarea', "");
  
        this.loadingInstance = this.starLoading();
  
        axios.post('/api/extractAVIDL', {
          fileNameAVI: this.fileNameAVI2,
          method: param,
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
  
  