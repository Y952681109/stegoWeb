const Layout = () => import(/* webpackChunkName: 'index' */ '../page/layout')

const staticRoute = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/error',
        component: () => import(/* webpackChunkName: 'error' */ '../page/error'),
        children: [
            {
                path: '401',
                component: () => import(/* webpackChunkName: 'error' */ '../page/error/401')
            },
            {
                path: '403',
                component: () => import(/* webpackChunkName: 'error' */ '../page/error/403')
            },
            {
                path: '404',
                component: () => import(/* webpackChunkName: 'error' */ '../page/error/404')
            },
            {
                path: '500',
                component: () => import(/* webpackChunkName: 'error' */ '../page/error/500')
            }
        ]
    },
    {
        path: '/login',
        component: () => import(/* webpackChunkName: 'login' */ '../page/login')
    },
    {
        path: '/home',
        component: Layout,
        children: [
            {
                path: '',
                component: () => import(/* webpackChunkName: 'home' */ '../page/home'),
            },
            {
                path: 'admin',
                component: () => import(/* webpackChunkName: 'components' */ '../page/home/index_admin')
            }
        ]
    },
    {
        path: '/components',
        component: Layout,
        children: [
            {
                path: '',
                component: () => import(/* webpackChunkName: 'components' */ '../page/components')
            },
            {
                path: 'pageNotes',
                component: () => import(/* webpackChunkName: 'components' */ '../page/components/assist/pageNotes')
            },
            {
                path: 'permission',
                component: () => import(/* webpackChunkName: 'components' */ '../page/components/function/permission')
            },
            {
                path: 'pageTable',
                component: () => import(/* webpackChunkName: 'components' */ '../page/components/function/pageTable')
            },
            {
                path: 'pageSearch',
                component: () => import(/* webpackChunkName: 'components' */ '../page/components/ui/pageSearch')
            },
            {
                path: 'pageSection',
                component: () => import(/* webpackChunkName: 'components' */ '../page/components/ui/pageSection')
            },
            {
                path: 'pageTitle',
                component: () => import(/* webpackChunkName: 'components' */ '../page/components/ui/pageTitle')
            },
            {
                path: 'pageToolbar',
                component: () => import(/* webpackChunkName: 'components' */ '../page/components/ui/pageToolbar')
            }
        ]
    },
    {
        path: '/example',
        component: Layout,
        children: [
            {
                path: 'table',
                component: () => import(/* webpackChunkName: 'example' */ '../page/example/table')
            },
            {
                path: 'charts',
                component: () => import(/* webpackChunkName: 'example' */ '../page/example/charts')
            },
            {
                path: 'map',
                component: () => import(/* webpackChunkName: 'example' */ '../page/example/map')
            }
        ]
    },
    {
        path: '/stego',
        component: Layout,
        children: [
            {
                path: 'jpgDL',
                component: () => import(/* webpackChunkName: 'example' */ '../page/stego/jpgDL')
            },
            {
                path: 'txtDL',
                component: () => import(/* webpackChunkName: 'example' */ '../page/stego/txtDL')
            },
            {
                path: 'wavDL',
                component: () => import(/* webpackChunkName: 'example' */ '../page/stego/wavDL')
            },
            {
                path: 'aviDL',
                component: () => import(/* webpackChunkName: 'example' */ '../page/stego/aviDL')
            }
        ]
    },
    {
        path: '/stego',
        component: Layout,
        children: [
            {
                path: 'bmp',
                component: () => import(/* webpackChunkName: 'example' */ '../page/stego/bmp')
            },
            {
                path: 'wav',
                component: () => import(/* webpackChunkName: 'example' */ '../page/stego/wav')
            },
            {
                path: 'mid',
                component: () => import(/* webpackChunkName: 'example' */ '../page/stego/mid')
            },
            {
                path: 'wma',
                component: () => import(/* webpackChunkName: 'example' */ '../page/stego/wma')
            },
            {
                path: 'mp4',
                component: () => import(/* webpackChunkName: 'example' */ '../page/stego/mp4')
            }
        ]
    },
    {
        path: '/record',
        component: Layout,
        children: [
            {
                path: 'history',
                component: () => import(/* webpackChunkName: 'example' */ '../page/record/history')
            },
            {
                path: 'type',
                component: () => import(/* webpackChunkName: 'example' */ '../page/record/type')
            },
            {
                path: 'statistics',
                component: () => import(/* webpackChunkName: 'example' */ '../page/record/statistics')
            }
        ]
    },
    {
        path: '/i18n',
        component: Layout,
        children: [
            {
                path: '',
                component: () => import(/* webpackChunkName: 'i18n' */ '../page/i18n')
            }
        ]
    },
    {
        path: '/theme',
        component: Layout,
        children: [
            {
                path: '',
                component: () => import(/* webpackChunkName: 'themeChange' */ '../page/themeChange')
            }
        ]
    },
    {
        path: '/n_home',
        component: Layout,
        children: [
            {
                path: '',
                component: () => import(/* webpackChunkName: 'themeChange' */ '../page/n_home')
            }
        ]
    },
    {
        path: '*',
        redirect: '/error/404'
    }
]

export default staticRoute