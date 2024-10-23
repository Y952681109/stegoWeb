<template>
  <div class="sys-page">
      <app-title title="算法简介"></app-title>
      <div class="page-content">
          <app-notes>
              <p>ECC编码：首先对秘密信息进行纠错编码，以增强信息在传输或存储过程中的鲁棒性。</p>
              <p>特征提取：对封面图像进行处理，提取其关键特征并将其转换为低维潜在表示。</p>
              <p>信息嵌入：将编码后的秘密信息与封面图像的潜在表示结合，通过修改潜在表示来隐藏信息。</p>
              <p>模型解码：将嵌入信息的潜在表示解码回像素空间，生成与原始封面图像相似的隐写图像。</p>
              <p>生成隐写图像：通过计算原始封面图像与隐写图像之间的微小残差，并将此残差应用到原始图像上，最终生成难以被察觉但包含秘密信息的隐写图像。</p>
          </app-notes>
          <app-section title="jpg图像嵌入">
              <div class="sys-article">
                  <p><strong>上传说明</strong></p>
                  <p>jpg图像嵌入只支持上传jpg图像作为载体，txt文本文件存放隐藏信息。</p>
                  <p>载体大小为1920*1080的条件下，嵌入极限为189B。算法嵌入率为0.0007bpp</p>
              </div>
              <el-row :gutter="20">
                <el-col :span="12">
                  <div class="sys-article">
                      <p><strong>载体图像</strong></p>
                  </div>
                  <el-upload
                      style="display: flex;justify-content: center;align-items: center;"
                      action="/api/upload"
                      list-type="picture"
                      :file-list="fileList1"
                      accept=".jpg"
                      :on-preview="handlePictureCardPreview"
                      :on-success="handleSuccessJPG"
                      :on-remove="handleRemoveJPG"
                      :limit="1">
                      <img v-if="imageUrl" :src="imageUrl" class="avatar">
                      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
                  <el-dialog :visible.sync="dialogVisible">
                      <img width="100%" :src="dialogImageUrl" alt="">
                  </el-dialog>
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



          <app-section title="jpg图像提取">
            <div class="sys-article">
                  <p><strong>上传说明</strong></p>
                  <p>jpg图像提取只支持上传jpg图像进行提取</p>
              </div>
              <el-row :gutter="20">
                <el-col :span="12">
                  <div class="sys-article">
                      <p><strong>待提取图像</strong></p>
                  </div>
                  <el-upload
                      style="display: flex;justify-content: center;align-items: center;"
                      action="/api/upload"
                      list-type="picture"
                      :file-list="fileList3"
                      accept=".jpg"
                      :on-preview="handlePictureCardPreview"
                      :on-success="handleSuccessJPG2"
                      :on-remove="handleRemoveJPG2"
                      :limit="1">
                      <img v-if="imageUrl" :src="imageUrl" class="avatar">
                      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
                  <el-dialog :visible.sync="dialogVisible">
                      <img width="100%" :src="dialogImageUrl" alt="">
                  </el-dialog>
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
        name: 'jpgDL',
        imageUrl: '',
        dialogImageUrl: '',
        dialogVisible: false,
        textarea: '',
        filelist1: [],
        filelist2: [],
        filelist3: [],
        fileNameJPG: null,
        fileNameTXT: null,
        fileNameJPG2: null,
    };
  },
  methods: {
    handleSuccessJPG2(response, file, fileList){
      console.log(response.filename)
      this.fileNameJPG2 = response.filename
    },
    handleRemoveJPG2(file, fileList) {
      this.fileNameJPG2 = null;
    },
    handleRemoveJPG(file, fileList) {
      this.fileNameJPG = null;
    },
    handleRemoveTXT(file, fileList) {
      this.fileNameTXT = null;
    },
    handleSuccessJPG(response, file, fileList){
      console.log(response.filename)
      this.fileNameJPG = response.filename
    },
    handleSuccessTXT(response, file, fileList){
      console.log(response.filename)
      this.fileNameTXT = response.filename
    },
    embed(param){
      console.log(this.fileNameJPG)
      console.log(this.fileNameTXT)
      console.log(param)

      // 检查fileJPG是否为null
      if (this.fileNameJPG === null) {
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

      // axios({
      //     url: '/api/embedJPG',
      //     method: 'post',
      //     data: {
      //         fileNameJPG: this.fileNameJPG,
      //         fileNameTXT: this.fileNameTXT,
      //     },
      //     responseType: 'blob' // 期望以blob格式接收数据
      // }).then((response) => {
      //     // 检查 response 是否是 Blob
      //     const url = URL.createObjectURL(new Blob([response], { type: 'image/jpeg' }));
      //     const link = document.createElement('a');
      //     link.href = url;
      //     link.setAttribute('download', 'filename.jpg'); // 自定义下载文件的名称
      //     document.body.appendChild(link);
      //     link.click();
      //     // 清理
      //     document.body.removeChild(link);
      //     window.URL.revokeObjectURL(url);
      // }).catch((error) => {
      //     console.error('Error during the request:', error);
      // });

      // 使用axios
      // 使用axios发送POST请求
      axios.post('/api/embedJPG', {
        fileNameJPG: that.fileNameJPG, // 你的请求参数
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
            link.setAttribute('download', 'stegoIMG.jpg'); // 指定下载的文件名
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
      console.log(this.fileNameJPG2);
      console.log(this.userId);
      console.log(this.username);
      console.log(this.user);
      console.log(param);

      // 检查fileJPG是否为null
      if (this.fileNameJPG2 === null) {
        alert("请先上传隐写图像");
        return; // 退出函数，不再执行后续代码
      }

      this.$set(this, 'textarea', "");

      this.loadingInstance = this.starLoading();

      axios.post('/api/extractJPG', {
        fileNameJPG: this.fileNameJPG2,
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

    // extract(){
    //   console.log(this.fileNameJPG2)

    //   console.log(this.userId)

    //   console.log(this.username)

    //   console.log(this.user)


    //   // 检查fileJPG是否为null
    //   if (this.fileNameJPG2 === null) {
    //       alert("请先上传隐写图像");
    //       return; // 退出函数，不再执行后续代码
    //   }


    //   var that = this;

    //   this.loadingInstance  = this.starLoading();

    //   var resp;


    //   // axios.post('/api/extractJPG', {  
    //   //   fileNameJPG: this.fileNameJPG2,  
    //   //   userId: this.userId  
    //   // }, {  
    //   //   responseType: 'blob' // 确保响应类型为blob  
    //   // })  
    //   // .then(response => {  
    //   //   // 检查 response.data 是否是 Blob 对象  
    //   //   const reader = new FileReader();
    //   //   reader.onload = (e) => { 
    //   //     try {
    //   //       const resData = JSON.parse(e.target.result); 
    //   //       console.log('JSON解析成功1:', resData);

    //   //       this.$notify.error({
    //   //         title: '错误',
    //   //         message: resData.message
    //   //       });

    //   //     } catch (error) {
    //   //       console.error('JSON解析失败11:11111111', error);
    //   //       this.$set(this, 'textarea', e.target.result);
    //   //       console.log(e.target.result);  

    //   //       // 创建一个可以下载的链接  
    //   //       const url = window.URL.createObjectURL(new Blob([response.data]));  
    //   //       const link = document.createElement('a');  
    //   //       link.href = url;  
    //   //       link.setAttribute('download', 'output.txt'); // 指定下载的文件名  
    //   //       document.body.appendChild(link);  
    //   //       link.click();  
    //   //       document.body.removeChild(link);  
    //   //       window.URL.revokeObjectURL(url); // 释放对象URL  
    //   //     } finally {
    //   //       this.$nextTick(() => {
    //   //         // 在 nextTick 之后关闭 loading
    //   //         this.loadingInstance.closeLoading();
    //   //       });
    //   //     }
    //   //   };
    //   //   reader.readAsText(response.data);
    //   // })  
    //   // .catch(error => {  
    //   //   console.error('出现错误！', error);  
    //   //   this.$nextTick(() => {
    //   //     // 在 nextTick 之后关闭 loading
    //   //     this.loadingInstance.closeLoading();
    //   //   });
    //   // });



    //   axios.post('/api/extractJPG', {  
    //     fileNameJPG: this.fileNameJPG2,  
    //     userId: this.userId  
    //   }, {  
    //     responseType: 'blob' // 确保响应类型为blob  
    //   })  
    //   .then(response => {  
    //     // 首先检查 response.data 是否是一个 Blob 对象  
    //     resp = response;
    //     try {
    //         // 尝试解析JSON字符串
    //         let reader = new FileReader()
    //         let resData = ""
    //         reader.readAsText(response)
    //         setTimeout(()=>{
    //           resData = JSON.parse(reader.result)
    //           console.log('JSON解析成功1:', resData);

    //           this.$notify.error({
    //             title: '错误',
    //             message: resData.message
    //           });

    //           this.$nextTick(() => {
    //           // 在 nextTick 之后关闭 loading
    //             this.loadingInstance.closeLoading();
    //           })
    //         },500)


    //     } catch (error) {
    //         // 如果解析失败，捕获异常，并执行备用方法或错误处理逻辑
    //         console.error('JSON解析失败11:11111111', error);
    //         // 这里可以定义跳转到其他方法的逻辑
    //         // 例如，调用一个错误处理函数或执行其他操作
    //         const reader = new FileReader();  
    //         reader.onload = (e) => { // 使用箭头函数来保持 this 的上下文  
    //           // this.textarea = e.target.result; // 使用 this 替代 that  
    //           this.$set(this, 'textarea', e.target.result)
    //           console.log(e.target.result);  
    //         };  
    //         reader.readAsText(response); // 使用 response.data 作为参数  

    //         // 创建一个可以下载的链接  
    //         const url = window.URL.createObjectURL(new Blob([response]));  
    //         const link = document.createElement('a');  
    //         link.href = url;  
    //         link.setAttribute('download', 'output.txt'); // 指定下载的文件名  
    //         document.body.appendChild(link);  
    //         link.click();  
    //         document.body.removeChild(link);  
    //         window.URL.revokeObjectURL(url); // 释放对象URL  

    //         this.$nextTick(() => {
    //         // 在 nextTick 之后关闭 loading
    //           this.loadingInstance.closeLoading();
    //         })
    //     }


    //   })  
    //   .catch(error => {  
    //     console.error('There was an error!111111111', error);  

    //     this.$nextTick(() => {
    //     // 在 nextTick 之后关闭 loading
    //       this.loadingInstance.closeLoading();
    //     })
    //   });

    //   console.log('There was an error!222222222');  





    //   // axios.post('/api/extractJPG', {  
    //   //   fileNameJPG: this.fileNameJPG2,  
    //   //   userId: this.userId  
    //   // }, {  
    //   //   responseType: 'blob' // 确保响应类型为blob  
    //   // })  
    //   // .then(response => {  
    //   //   // 首先检查 response.data 是否是一个 Blob 对象  
    //   //   if (response instanceof Blob) {  
    //   //     // 使用 FileReader 读取 Blob 内容  
    //   //     const reader = new FileReader();  
    //   //     reader.onload = (e) => { // 使用箭头函数来保持 this 的上下文  
    //   //       // this.textarea = e.target.result; // 使用 this 替代 that  
    //   //       this.$set(this, 'textarea', e.target.result)
    //   //       console.log(e.target.result);  
    //   //     };  
    //   //     reader.readAsText(response); // 使用 response.data 作为参数  
    //   //   } else {  
    //   //     console.error('响应数据不是一个 Blob 对象');  
    //   //   }  

    //   //   this.$forceUpdate()
      
    //   //   // 创建一个可以下载的链接  
    //   //   const url = window.URL.createObjectURL(new Blob([response]));  
    //   //   const link = document.createElement('a');  
    //   //   link.href = url;  
    //   //   link.setAttribute('download', 'output.txt'); // 指定下载的文件名  
    //   //   document.body.appendChild(link);  
    //   //   link.click();  
    //   //   document.body.removeChild(link);  
    //   //   window.URL.revokeObjectURL(url); // 释放对象URL  

    //   //   this.$nextTick(() => {
    //   //   // 在 nextTick 之后关闭 loading
    //   //     this.loadingInstance.closeLoading();
    //   //   })

    //   // })  
    //   // .catch(error => {  
    //   //   console.error('There was an error!', error);  

    //   //   this.$nextTick(() => {
    //   //   // 在 nextTick 之后关闭 loading
    //   //     this.loadingInstance.closeLoading();
    //   //   })
    //   // });


    // },

    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
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

