<template>
    <div class="sys-page">
        <app-title title="历史记录"></app-title>
        <!-- 搜索 -->
        <app-search>
            <el-form :inline="true" :model="searchForm">
                <el-form-item>
                    <el-date-picker v-model="searchForm.time" type="date" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item>
                    <el-select v-model="searchForm.type" placeholder="下拉选择">
                        <el-option label="jpgDL嵌入" value="1"></el-option>
                        <el-option label="jpgDL解析" value="2"></el-option>
                        <el-option label="txtDL嵌入" value="3"></el-option>
                        <el-option label="txtDL解析" value="4"></el-option>
                        <el-option label="wavDL嵌入" value="5"></el-option>
                        <el-option label="wavDL解析" value="6"></el-option>
                        <el-option label="aviDL嵌入" value="7"></el-option>
                        <el-option label="aviDL解析" value="8"></el-option>
                        <el-option label="wav嵌入" value="9"></el-option>
                        <el-option label="wav解析" value="10"></el-option>
                        <el-option label="wma嵌入" value="11"></el-option>
                        <el-option label="wma解析" value="12"></el-option>
                        <el-option label="mid嵌入" value="13"></el-option>
                        <el-option label="mid解析" value="14"></el-option>
                        <el-option label="mp4嵌入" value="15"></el-option>
                        <el-option label="mp4解析" value="16"></el-option>
                        <el-option label="bmp嵌入" value="17"></el-option>
                        <el-option label="bmp解析" value="18"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="search">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="clear">清空</el-button>
                </el-form-item>
            </el-form>
        </app-search>
        <!-- 表格体 -->
        <table-mixin pagination paginationAlign="center" :paginationTotal="pageTotal" :pageSize="pageSize"
            :currentPage="currentPage" :sizeChange="handleSizeChange" :pageChange="handleCurrentChange">
            <el-table v-loading="tableData.loading" :data="tableData.body" border
                :default-sort="{ prop: 'date', order: 'descending' }">
                <el-table-column type="index" label="序号" width="64" align="center"></el-table-column>
                <el-table-column v-for="(item, index) in tableData.head" :prop="item.key" :label="item.name" sortable
                    :key="index"></el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button v-if="scope.row.operation.indexOf('download') >= 0" type="text" size="small"
                            @click="download(scope.row.recordRemark)">下载</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </table-mixin>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'exampleTable',
    computed: {
        ...mapState({
            userId: state => state.user.uid,
            username: state => state.user.name,
            user: state => state.user
        })
    },
    data() {
        return {
            searchForm: {
                time: '',
                type: ''
            },
            tableData: {
                loading: true,
                head: [],
                body: []
            },
            pageTotal: 30,
            pageSize: 10,
            currentPage: 1
        }
    },
    mounted() {
        this.getTableData()
        this.getTableDataCount()
    },
    methods: {

        getTableData() {

            const params = {
                userId: this.userId,
                pageSize: this.pageSize,
                currentPage: this.currentPage,
                time: this.searchForm.time,
                type: this.searchForm.type
            };

            // 移除params对象中值为空的属性
            Object.keys(params).forEach(key => {
                if (params[key] === '') {
                    delete params[key];
                }
            });

            this.$axios({
                url: '/api/getHistory',
                type: 'get',
                params: params // 将构建的params对象作为请求参数
            }).then(res => {
                this.tableData.loading = false
                this.tableData.head = res.head
                this.tableData.body = res.body
            }).catch(err => {
                this.$message.error(`getHistory失败，失败码：${err}`)
            })


        },

        getTableDataCount() {

            const params = {
                userId: this.userId,
                time: this.searchForm.time,
                type: this.searchForm.type
            };

            // 移除params对象中值为空的属性
            Object.keys(params).forEach(key => {
                if (params[key] === '') {
                    delete params[key];
                }
            });

            this.$axios({
                url: '/api/getHistoryCount',
                type: 'get',
                params: params // 将构建的params对象作为请求参数
            }).then(res => {
                console.log(res)
                console.log(res.count)
                this.pageTotal = res.count
            }).catch(err => {
                console.error(err)
                // this.$message.error(`getHistoryCount失败，失败码：${err.response.status}`)
            })
        },
        search() {
            console.log(`欲提交的数据   日期:${this.searchForm.time}  下拉条件:${this.searchForm.type}`)
            this.getTableDataCount()
            this.getTableData()
        },
        clear() {
            this.searchForm.time = ''
            this.searchForm.type = ''
            this.getTableData()
            this.getTableDataCount()
        },
        download(filepath) {

            let parts = filepath.split('/'); // 使用'/'分割字符串
            let fileNameWithExtension = parts[parts.length - 1]; // 获取最后一个部分

            this.$axios({
                url: '/api/download',
                method: 'get',
                params: {
                    filepath: filepath
                },
                responseType: 'blob',   // 重要：设置响应类型为blob
            }).then((response) => {
                console.log(response)
                const url = window.URL.createObjectURL(new Blob([response]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', fileNameWithExtension); // 指定下载的文件名
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

            }).catch((error) => {
                console.error('Error during the request:', error);
            });

        },
        handleSizeChange(newSize) {
            console.log("sizeChange!!")
            this.pageSize = newSize;
            console.log(newSize)

            this.getTableData()
        },
        handleCurrentChange(newPage) {
            console.log("pageChange!!")
            this.currentPage = newPage;
            console.log(newPage)

            this.getTableData()
        }
    }
}
</script>