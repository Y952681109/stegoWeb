var data = [
    {
        path: '/home',
        name: '首页'
    },
    {
        name: '系统组件',
        child: [
            {
                name: '介绍',
                path: '/components'
            },
            {
                name: '功能类',
                child: [
                    {
                        path: '/components/permission',
                        name: '详细鉴权'
                    },
                    {
                        path: '/components/pageTable',
                        name: '表格分页'
                    }
                ]
            },
            {
                name: '布局类',
                child: [
                    {
                        path: '/components/pageTitle',
                        name: '页面标题'
                    },
                    {
                        path: '/components/pageSection',
                        name: '子区域'
                    },
                    {
                        path: '/components/pageSearch',
                        name: '搜索条'
                    },
                    {
                        path: '/components/pageToolbar',
                        name: '工具条'
                    }
                ]
            },
            {
                name: '辅助类',
                child: [
                    {
                        path: '/components/pageNotes',
                        name: '引用说明'
                    }
                ]
            }
        ]
    },
    {
        name: '完整示例',
        child: [
            {
                path: '/example/table',
                name: '列表页面',
                permission: ['edit']
            },
            {
                path: '/example/charts',
                name: '图表页面'
            },
            {
                path: '/example/map',
                name: '地图页面'
            }
        ]
    },
    {
        name: '深度学习算法',
        child: [
            {
                path: '/stego/jpgDL',
                name: 'jpg图像'
            },
            {
                path: '/stego/txtDL',
                name: 'txt生成式文本'
            },
            {
                path: '/stego/wavDL',
                name: 'wav音频'
            },
            {
                path: '/stego/aviDL',
                name: 'avi视频'
            }
        ]
    },
    {
        name: '记录查询',
        child: [
            {
                path: '/record/statistics',
                name: '使用统计'
            },
            {
                path: '/record/history',
                name: '历史记录'
            }
        ]
    },
    {
        path: '/i18n',
        name: '国际化'
    },
    {
        path: '/theme',
        name: '主题切换'
    },
    {
        path: '/n_home',
        name: '新的首页'
    },
    {
        path: '/n_task',
        name: '任务队列'
    },
    {
        name: '使用统计',
        child: [
            {
                path: '/statistics/table',
                name: '列表页面',
                permission: ['edit']
            },
            {
                path: '/statistics/charts',
                name: '图表页面'
            },
            {
                path: '/statistics/map',
                name: '地图页面'
            }
        ]
    }
]

export default [{
    path: '/user/navlist',
    data: data
}]