<template>
    <div class="sys-page">
        <app-title title="类型统计"></app-title>
        <chart2 :chartData="chartData"></chart2>
    </div>
  </template>
  
  <script>
  import Chart2 from './chart2'
  import axios from '@/util/ajax'
  import { mapState } from 'vuex'
  
  export default {
    name: 'type',
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
                url: '/api/getStatisticsType',
                method: 'get',
                params: {
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
    components: {Chart2}
  }
  </script>