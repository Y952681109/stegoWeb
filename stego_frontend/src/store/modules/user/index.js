import Cookies from 'js-cookie'

const state = {
    // 用户名
    name: '',
    uid: ''
}

const mutations = {
    setName: (state, data) => {
        console.log("setName")
        console.log("setName - state", state)
        console.log("setName - data", data)
        if(data){
            Cookies.set('userName', encodeURIComponent(data), {
                expires: 365
            })
        } else {
            Cookies.remove('userName')
        }
        state.name = data
    },

    setUid: (state, data) => {
        console.log("setUid")
        console.log("setUid - state", state)
        console.log("setUid - data", data)
        if(data){
            Cookies.set('userId', encodeURIComponent(data), {
                expires: 365
            })
        } else {
            Cookies.remove('userId')
        }
        state.uid = data
    }
}

export default {
    namespaced: true,
    state,
    mutations
}