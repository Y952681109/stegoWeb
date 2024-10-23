<template>
  <div class="sys-page">
      <app-title title="使用次数"></app-title>
        <!-- <app-toolbar>
            <el-button type="primary" @click="getChartData">刷新数据</el-button>
        </app-toolbar> -->
        <chart1 :chartData="chartData"></chart1>
  </div>
</template>

<script>
import Chart1 from './chart1'
import axios from '@/util/ajax'
import { mapState } from 'vuex'

export default {
  name: 'exampleChart',
  data(){
      return {
          chartData: [],
          chart: []
      }
  },
  mounted(){
      this.$nextTick(() => {
          this.getChartData()
      })
  },
  computed: {
        ...mapState({
          userId: state => state.user.uid,
          username: state => state.user.name,
          user: state => state.user
        })
  },
  methods: {
      getChartData(){
        var that = this;

        console.log(that.userId)

        this.$axios({
              url: '/api/getStatistics',
              method: 'get',
              params: {
                  days: 7,
                  userId: that.userId
              },
          }).then((response) => {
            console.log(response)
            this.chartData = response



          }).catch((error) => {
              console.error('Error during the request:', error);
          });
      }


  },
  components: {Chart1}
}
</script>