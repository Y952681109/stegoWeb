<template>
    <div class="sys-page">
        <app-title title="主题变更"></app-title>
        <div class="page-content">
            <app-section title="切换布局">
                <div class="layout-list">
                    <ul>
                        <li :class="layout == 'top' ? 'cur' : ''" @click="changeTheme('top')">
                            <img src="~sysStatic/images/layout-top.png" alt="">
                            <p>上下布局</p>
                        </li>
                        <li :class="layout == 'left' ? 'cur' : ''" @click="changeTheme('left')">
                            <img src="~sysStatic/images/layout-left.png" alt="">
                            <p>左右布局</p>
                        </li>
                    </ul>
                </div>
            </app-section>
        </div>
    </div>
</template>

<script>
export default{
    name: 'themeChange',
    computed: {
        layout(){
            return this.$store.state.navbarPosition
        }
    },
    methods: {
        changeTheme(data){
            this.$store.commit("setLayout", data)
        }
    }
}
</script>

<style lang="scss" scoped>
.layout-list{
    &:after{
        clear: both;
        overflow: hidden;
    }
    ul{
        padding: 5px;
        overflow: hidden;
    }
    ul li{
        float: left;
        background: #fff;
        margin-right: 20px;
        padding: 10px;
        box-shadow: 0 0 3px #ccc;
        &:hover, &.cur:hover{
            box-shadow: 0 0 10px #ccc;
        }
        &.cur{
            border: 1px solid #ccc;
            box-shadow: none;
        }
        img{
            width: 140px;
        }
        p{
            height: 40px;
            line-height: 40px;
            text-align: center;
            font-size: 14px;
        }
    }
}
</style>