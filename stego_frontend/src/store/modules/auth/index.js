import Cookies from 'js-cookie'
import axios from '@/util/ajax'
import Auth from '@/util/auth'
import { EventBus } from "../../../event-bus.js";

const state = {
    token: '',
    navList: [],
    uid: ''
}

const mutations = {
    setNavList: (state, data) => {
        state.navList = data
    },

    setToken: (state, data) => {
        console.log("login - setToken")
        console.log(state)
        console.log(data)
        if(data){
            Auth.setToken(data)
            Auth.setLoginStatus()
        } else {
            Auth.removeToken()
            Auth.removeLoginStatus()
        }
        state.token = data
    },

    setUid: (state, data) => {
        state.uid = data
    }
}

const actions = {
    // 邮箱登录
    loginByEmail({ commit }, userInfo) {
        console.log("login - start")
        return new Promise((resolve) => {
            axios({
                url: '/api/login123',
                method: 'post',
                data: {
                    ...userInfo
                }
            }).then(res => {
                console.log("login - res")
                console.log(res)
                if(res.login){
                    console.log("login - login true")
                    console.log(res.token)
                    console.log(res.name)
                    commit('setToken', res.token)
                    commit('setUid', res.uid)
                    commit('user/setName', res.name, { root: true })
                    commit('user/setUid', res.uid, { root: true })
                }
                resolve(res)
            })
        });
    },

    // loginByEmail({ commit }, userInfo) {
    //     return new Promise((resolve) => {
    //         axios({
    //             url: '/login',
    //             method: 'post',
    //             data: {
    //                 ...userInfo
    //             }
    //         }).then(res => {
    //             if(res.login){
    //                 commit('setToken', res.token)
    //                 commit('user/setName', res.name, { root: true })
    //             }
    //             resolve(res)
    //         })
    //     });
    // },

    // 登出
    logout({commit}) {
        return new Promise((resolve) => {
            commit('setToken', '')
            commit('setUid', '')
            commit('user/setName', '', { root: true })
            commit('user/setUid', '', { root: true })
            commit('tagNav/removeTagNav', '', {root: true})
            EventBus.$emit('user-logout');
            resolve()
        })
    },

    // 重新获取用户信息及Token
    // TODO: 这里不需要提供用户名和密码，实际中请根据接口自行修改
    relogin({dispatch, commit, state}){
        return new Promise((resolve) => {
            // 根据Token进行重新登录
            let token = Cookies.get('token'),
                userName = Cookies.get('userName')
                userId = Cookies.get('userId')

            // 重新登录时校验Token是否存在，若不存在则获取
            if(!token){
                dispatch("getNewToken").then(() => {
                    commit('setToken', state.token)
                })
            } else {
                commit('setToken', token)
            }
            // 刷新/关闭浏览器再进入时获取用户名
            commit('user/setName', decodeURIComponent(userName), { root: true })
            commit('user/setUid', decodeURIComponent(userId), { root: true })
            resolve()
        })
    },

    // 获取新Token
    getNewToken({commit, state}){
        return new Promise((resolve) => {
            axios({
                url: '/getToken',
                method: 'get',
                param: {
                    token: state.token
                }
            }).then((res) =>{
                commit("setToken", res.token)
                resolve()
            })
        })
    },

    // 获取该用户的菜单列表
    // getNavList({commit}){
    //     return new Promise((resolve) =>{
    //         axios({
    //             url: '/user/navlist',
    //             methods: 'post',
    //             data: {}
    //         }).then((res) => {
    //             commit("setNavList", res)
    //             resolve(res)
    //         })
    //     })
    // },

    getNavList({commit}){
        return new Promise((resolve, reject) =>{
            let userId = state.uid

            console.log('userId + ', userId)

            

            let rad = Math.random()

            axios({
                url: '/api/getNavlist',
                method: 'get',
                params: {
                    userId: userId,
                    rad: rad
                }
            }).then((res) => {
                commit("setNavList", res)
                resolve(res)
            })
            .catch(error => {
                console.log('Error occurred:', error);
                if (error.response) {
                    console.log('Server responded with error:', error.response.status, error.response.data);
                } else if (error.request) {
                    console.log('No response received:', error.request);
                } else {
                    console.log('Error setting up request:', error.message);
                }
                reject(error);  // This line should now work correctly
            });
        })
    },

    // 将菜单列表扁平化形成权限列表
    getPermissionList({state}){
        return new Promise((resolve) =>{
            let permissionList = []
            // 将菜单数据扁平化为一级
            function flatNavList(arr){
                for(let v of arr){
                    if(v.child && v.child.length){
                        flatNavList(v.child)
                    } else{
                        permissionList.push(v)
                    }
                }
            }

            console.log("=============")
            console.log(permissionList)

            flatNavList(state.navList)
            resolve(permissionList)
        })
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}