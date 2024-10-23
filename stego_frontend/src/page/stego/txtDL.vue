<template>
    <div class="sys-page">
        <app-title title="算法简介"></app-title>
        <div class="page-content">
            <app-notes>
                <p>自适应调整：算法动态调整参数K，这个参数决定了在每一步编码过程中考虑的候选词的数量。这种调整基于当前上下文的词分布，以实现最优的不可感知性。</p>
                <p>算术编码：SAAC使用算术编码技术将秘密信息的二进制序列编码成文本。在每一步中，算法根据神经语言模型计算下一个词的条件分布，并根据这个分布和秘密信息来选择下一个词。</p>
                <p>统计不可感知性：算法设计的目标是使得生成的文本在统计上与自然语言模型输出的文本分布尽可能接近，以避免引起潜在监听者的怀疑。</p>
            </app-notes>
            <app-section title="txt文本嵌入">
                <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>txt生成式文本嵌入只支持上传txt文本文件作为载体，txt文本文件存放秘密信息，返回嵌入后的txt格式加密文件</p>
                    <p>在载体大小为1439B(216单词)的条件下，可以嵌入80B信息。嵌入率为2.96bpw</p>
                </div>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>载体文本</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".txt"
                        :file-list="fileList1"
                        :on-success="handleSuccessTXT"
                        :on-remove="handleRemoveTXT"
                        multiple
                        :limit="1">
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    </el-upload>
                  </el-col>
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>嵌入文本</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".txt"
                        :file-list="fileList2"
                        :on-success="handleSuccessTXT2"
                        :on-remove="handleRemoveTXT2"
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
  
  
  
            <app-section title="txt文本提取">
              <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>txt文本提取需要首先上传加密前的载体文件和嵌入后包含隐藏信息的加密文件，返回输出解密后的秘密信息</p>
                </div>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>原始文本</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".txt"
                        :file-list="fileList3"
                        :on-success="handleSuccessTXT3"
                        :on-remove="handleRemoveTXT3"
                        multiple
                        :limit="1">
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    </el-upload>
                  </el-col>
                  <el-col :span="12">
                    <div class="sys-article">
                        <p><strong>隐藏后文本</strong></p>
                    </div>
                    <el-upload
                        class="upload-demo"
                        style="display: flex;justify-content: center;align-items: center;"
                        drag
                        action="/api/upload"
                        accept=".txt"
                        :file-list="fileList4"
                        :on-success="handleSuccessTXT4"
                        :on-remove="handleRemoveTXT4"
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
          name: 'txtDL',
          filelist1: [],
          filelist2: [],
          filelist3: [],
          filelist4: [],
          fileNameTXT: null,
          fileNameTXT2: null,
          fileNameTXT3: null,
          fileNameTXT4: null,
      };
    },
    methods: {
      handleSuccessTXT(response, file, fileList){
        console.log(response.filename)
        this.fileNameTXT = response.filename
      },
      handleSuccessTXT2(response, file, fileList){
        console.log(response.filename)
        this.fileNameTXT2 = response.filename
      },
      handleSuccessTXT3(response, file, fileList){
        console.log(response.filename)
        this.fileNameTXT3 = response.filename
      },
      handleSuccessTXT4(response, file, fileList){
        console.log(response.filename)
        this.fileNameTXT4 = response.filename
      },
      handleRemoveTXT(file, fileList) {
        this.fileNameTXT = null;
      },
      handleRemoveTXT2(file, fileList) {
        this.fileNameTXT2 = null;
      },
      handleRemoveTXT3(file, fileList) {
        this.fileNameTXT3 = null;
      },
      handleRemoveTXT4(file, fileList) {
        this.fileNameTXT4 = null;
      },
      embed(){
        console.log(this.fileNameTXT)
        console.log(this.fileNameTXT2)
  
        // 检查fileJPG是否为null
        if (this.fileNameTXT === null) {
            alert("请先上传载体文本");
            return; // 退出函数，不再执行后续代码
        }
  
        // 检查fileTXT是否为null
        if (this.fileNameTXT2 === null) {
            alert("请先上传隐藏信息");
            return; // 退出函数，不再执行后续代码
        }
  
        var that = this;
  
        this.loadingInstance  = this.starLoading();
  
        axios.post('/api/embedTXT', {
          fileNameTXT: that.fileNameTXT, // 你的请求参数
          fileNameTXT2: that.fileNameTXT2,
          userId: that.userId
        }, {
          responseType: 'blob' // 指定响应类型为blob
        })
        .then(response => {
          console.log(response)
          const url = window.URL.createObjectURL(new Blob([response]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'stegoTXT.txt'); // 指定下载的文件名
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
  
  
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
        if (this.fileNameTXT3 === null) {
          alert("请先上传原始文本");
          return; // 退出函数，不再执行后续代码
        }

        // 检查fileJPG是否为null
        if (this.fileNameTXT4 === null) {
          alert("请先上传隐写文本");
          return; // 退出函数，不再执行后续代码
        }
  
        this.$set(this, 'textarea', "");
  
        this.loadingInstance = this.starLoading();
  
        axios.post('/api/extractTXT', {
          fileNameTXT: this.fileNameTXT3,
          fileNameTXT2: this.fileNameTXT4,
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
  
  