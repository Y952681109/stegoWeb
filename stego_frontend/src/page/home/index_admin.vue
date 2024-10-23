<template>
    <div class="sys-page" v-once>
        <app-title title="后端管理系统"></app-title>
        <div class="page-content">
            <app-notes>
                <p>后端管理系统整体介绍</p>
                <p>后端提供功能列举</p>
                <p>其他内容</p>
            </app-notes>
            <app-section title="左边导航栏表标题">
                <div class="sys-article">
                    <p><strong>重点加粗</strong>介绍每个模块功能</p>
                </div>
            </app-section>
            <app-section title="左边导航栏表标题">
                <div class="sys-article">
                    <p><strong>重点加粗</strong>介绍每个模块功能</p>
                </div>
            </app-section>
        </div>
    </div>
</template>

<script>
export default {
    name: 'home'
}
</script>