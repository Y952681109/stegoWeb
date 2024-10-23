<template>
    <div id="chart1" class="chart-area"></div>
</template>

<script>
import echarts from 'echarts'
import '@/util/echarts.theme.default'

export default {
    data() {
        return {
            chart: {
                target: null,
                option: {
                    title: {
                        text: '使用记录',
                        subtext: '类型统计',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left'
                    },
                    series: []
                }
            }
        }
    },
    props: {
        chartData: Array
    },
    watch: {
        chartData(){
            if(this.chartData.length){
                this.draw()  
            }
        }
    },
    mounted(){
        this.$nextTick(() => {
            this.chartsInit()
            this.updateXAxisData();
        })
    },
    methods: {
        // 初始化图表
        chartsInit(){
            // 创建图表对象
            if(!this.chart.target){
                this.chart.target = echarts.init(document.getElementById('chart1'), 'westeros')
            }
            // 绘制默认图表
            this.chart.target.setOption(this.chart.option)
        },
        // 重绘
        draw() {
            // 配置项需要变更
            let option = {
                series: [
                    {
                        name: 'Access From',
                        type: 'pie',
                        radius: '50%',
                        data: this.chartData,
                        emphasis: {
                            itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            }
            this.chart.target.setOption(option)
        },

        updateXAxisData() {
            let date = new Date();
            let options = this.chart.target.getOption();
            let xAxisData = [];

            for (let i = 0; i < 7; i++) {
                // 复制日期对象以避免修改原始日期
                let tempDate = new Date(date);
                // 向前推i天
                tempDate.setDate(date.getDate() - i);
                // 格式化日期为 "x月x日" 的形式
                let month = tempDate.getMonth() + 1; // getMonth() 返回0-11，所以需要+1
                let day = tempDate.getDate();
                let formattedDate = `${month}月${day}日`;
                xAxisData.unshift(formattedDate); // 将日期插入数组的开头
            }

            console.log(xAxisData)

            options.xAxis[0].data = xAxisData;
            this.chart.target.setOption(options);
        }
    }
}
</script>

<style lang="scss" scoped>
.chart-area{
    width: 100%;
    height: 400px;
}
</style>