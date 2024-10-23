<template>
    <div class="sys-page">
        <app-title title="算法简介"></app-title>
        <div class="page-content">
            <app-notes>
                <p>读取MIDI文件：使用解析器加载MIDI文件，解析文件中的轨道和事件。</p>
                <p>选择嵌入位置：确定秘密信息嵌入的位置，通常选择对听觉影响较小的事件，如音符的细微调整、控制变化的微小变化等。</p>
                <p>编码秘密信息：使用特定的位模式或数据序列将秘密信息编码为可以嵌入到MIDI消息中的格式。</p>
                <p>嵌入信息：修改音符的音高、持续时间、控制器值等参数的值来在MIDI消息中嵌入秘密信息。</p>
            </app-notes>
            <app-section title="mid音频嵌入">
                <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>mid音频嵌入只支持上传mid音频作为载体，txt文本文件存放隐藏信息</p>
                    <p>载体大小为111KB的条件下可以嵌入14B信息。嵌入率为0.01%</p>
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
                        accept=".mid"
                        :file-list="fileList1"
                        :on-success="handleSuccessMID"
                        :on-remove="handleRemoveMID"
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
  
  
  
            <app-section title="mid音频提取">
              <div class="sys-article">
                    <p><strong>上传说明</strong></p>
                    <p>mid音频提取只支持上传mid音频进行提取</p>
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
                        accept=".mid"
                        :file-list="fileList3"
                        :on-success="handleSuccessMID2"
                        :on-remove="handleRemoveMID2"
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
          name: 'mid',
          textarea: '',
          filelist1: [],
          filelist2: [],
          filelist3: [],
          fileNameMID: null,
          fileNameTXT: null,
          fileNameMID2: null,
      };
    },
    methods: {
      handleSuccessMID2(response, file, fileList){
        console.log(response.filename)
        this.fileNameMID2 = response.filename
      },
      handleRemoveMID2(file, fileList) {
        this.fileNameMID2 = null;
      },
      handleRemoveMID(file, fileList) {
        this.fileNameMID = null;
      },
      handleRemoveTXT(file, fileList) {
        this.fileNameTXT = null;
      },
      handleSuccessMID(response, file, fileList){
        console.log(response.filename)
        this.fileNameMID = response.filename
      },
      handleSuccessTXT(response, file, fileList){
        console.log(response.filename)
        this.fileNameTXT = response.filename
      },
      embed(){
        console.log(this.fileNameMID)
        console.log(this.fileNameTXT)
  
        // 检查fileJPG是否为null
        if (this.fileNameMID === null) {
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
        axios.post('/api/embedMID', {
          fileNameMID: that.fileNameMID, // 你的请求参数
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
              link.setAttribute('download', 'stegoMID.mid'); // 指定下载的文件名
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
        if (this.fileNameMID2 === null) {
          alert("请先上传隐写图像");
          return; // 退出函数，不再执行后续代码
        }
  
        this.$set(this, 'textarea', "");
  
        this.loadingInstance = this.starLoading();
  
        axios.post('/api/extractMID', {
          fileNameMID: this.fileNameMID2,
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
  
  