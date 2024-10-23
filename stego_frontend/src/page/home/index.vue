<template>
    <div class="sys-page" v-once>
        <app-title title="信息隐藏系统"></app-title>
        <div class="page-content">
            <app-notes>
                <p>信息隐藏是一种技术，它允许在数字媒体（如图像、音频、视频或文本文件）中嵌入隐蔽的信息。这种技术通常用于保护版权、验证文件的真实性或在不引起注意的情况下传递秘密信息。</p>
                <p>在本系统中，主要实现了对不同类型不同格式的载体进行信息的隐藏和提取。</p>
                <p>其他功能包括查看操作数据、系统设置等</p>
            </app-notes>
            <app-section title="深度学习算法">
                <div class="sys-article">
                    <p>在该目录中，包含4个深度学习的隐藏提取算法</p>
                    <p>分别为<strong>jpg图像</strong>、<strong>avi视频</strong>、<strong>wav音频</strong>和<strong>txt文本</strong>四种不同类型的深度学习隐写及提取算法</p>
                </div>
            </app-section>
            <app-section title="非深度学习算法">
                <div class="sys-article">
                    <p>在该目录中，包含5个非深度学习的隐藏提取算法</p>
                    <p>分别为<strong>bmp图像</strong>、<strong>mp4视频</strong>、<strong>wav音频</strong>、<strong>mid音频</strong>和<strong>wma音频</strong>五种不同类型的隐写及提取算法</p>
                </div>
            </app-section>
            <app-section title="记录查询">
                <div class="sys-article">
                    <p><strong>使用次数</strong>使用线形图统计最近7天的使用数量</p>
                    <p><strong>类型统计</strong>使用饼状图统计系统不同算法嵌入的使用类别</p>
                    <p><strong>历史记录</strong>以表格形式显示所有的使用记录，并可以下载之前的输出文件</p>
                </div>
            </app-section>
            <app-section title="系统设置">
                <div class="sys-article">
                    <p>主要包括对系统整体布局的切换选择</p>
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