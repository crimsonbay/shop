import Vue from 'vue'
import Vuex from 'vuex'
import {
  SET_FIRST_NAME,
  CLEAR_FIRST_NAME,
  SET_TOKEN,
  CLEAR_TOKEN,
  SET_PAGE_NAME,
  SET_MENU,
  SET_CATEGORY_OVERVIEW
} from './mutation-types.js'
import { fetchCheckToken, fetchObtainToken, fetchRefreshToken, fetchGetMenu,
  fetchGetCategoryOverview } from '../api'
let jwtDecode = require('jwt-decode')

Vue.use(Vuex)

const state = {
  token: sessionStorage.getItem('token'), // user token (токен пользователя)
  firstName: sessionStorage.getItem('firstName'), // user first_name( first_name пользователя)
  pageName: '', // the name of the opened page( имя открытой страницы)
  menu: [], // category menu
  categoryOverview: null // detailed category menu
}

const getters = {
  TOKEN: state => {
    if (state.token) {
      return state.token
    } else {
      return null
    }
  },
  FIRST_NAME: state => {
    if (state.firstName) {
      return state.firstName
    } else {
      sessionStorage.setItem('firstName', 'Anonymous')
      return 'Anonymous'
    }
  },
  PAGE_NAME: state => state.pageName,
  MENU: state => state.menu,
  CATEGORY_OVERVIEW: state => state.categoryOverview
}

const mutations = {
  [SET_PAGE_NAME] (state, pageName) {
    state.pageName = pageName
  },
  [SET_TOKEN] (state, token) {
    sessionStorage.setItem('token', token)
    state.token = token
    window.location.reload(true)
  },
  [CLEAR_TOKEN] (state) {
    sessionStorage.removeItem('token')
    state.token = null
    window.location.reload(true)
  },
  [CLEAR_FIRST_NAME] (state) {
    sessionStorage.setItem('firstName', 'Anonymous')
    state.firstName = 'Anonymous'
  },
  [SET_FIRST_NAME] (state, firstName) {
    state.firstName = firstName
    sessionStorage.setItem('firstName', firstName)
  },
  [SET_MENU] (state, menu) {
    state.menu = menu
  },
  [SET_CATEGORY_OVERVIEW] (state, categoryOverview) {
    state.categoryOverview = categoryOverview
  }
}

const actions = {
  // set categoryOverview with categories without parent, the base categories
  // # witch main children with count of products in children and sub-children
  setCategoryOverview: ({commit}) => {
    fetchGetCategoryOverview().then(function (obj) {
      if (obj.status === 200) {
        commit(SET_CATEGORY_OVERVIEW, obj.body.results)
      }
      return obj
    }).catch(console.error.bind(console))
  },
  // set Main Categories menu
  setMenu: ({commit}) => {
    fetchGetMenu().then(function (obj) {
      if (obj.status === 200) {
        commit(SET_MENU, obj.body.results)
      }
      return obj
    }).catch(console.error.bind(console))
  },

  // set the name of the opened page( уcтановить имя открытой страницы)
  setPageName: ({commit}, {pageName}) => {
    commit(SET_PAGE_NAME, pageName)
    return 0
  },

  // clear token( очистить токен)
  clearToken: ({commit}) => {
    commit(CLEAR_TOKEN)
    // !!!window.location.reload(true)
    return 0
  },

  // check token, if ok, set the firstName for the token that came,
  // otherwise, erase the token and set the name Anonymous
  // (проверка токена, если ок, устанавливаем пришедший firstName для токена,
  // иначе стираем токен и устанавливаем имя Anonymous)
  checkToken: ({dispatch, commit, state, getters}) => {
    let token = getters.TOKEN
    if (token === null) {
      commit(CLEAR_FIRST_NAME)
      return 0
    }
    fetchCheckToken(token).then(function (obj) {
      if (obj.status === 200) {
        commit(SET_FIRST_NAME, obj.body.firstName)
      } else {
        commit(CLEAR_FIRST_NAME)
        commit(CLEAR_TOKEN)
      }
      return obj
    }).catch(console.error.bind(console))
  },

  // set the token by name and password, if the name and password are incorrect,
  // then the token is empty and the name is Anonymous
  // (установить токен по имени и паролю, если имя и пароль неверные, то токен пустой и имя Anonymous)
  setToken: ({dispatch, commit}, {username, password}) => {
    fetchObtainToken(username, password).then(function (obj) {
      if (obj.status === 200) {
        commit(SET_TOKEN, obj.body.token)
      } else {
        commit(CLEAR_FIRST_NAME)
        commit(CLEAR_TOKEN)
      }
      return obj
    }).then(function (obj) {
      dispatch('checkToken')
      // !!!window.location.reload(true)
      return obj
    }).catch(console.error.bind(console))
  },
  // refresh token
  refreshToken: ({dispatch, commit, getters}) => {
    let token = getters.TOKEN
    fetchRefreshToken(token).then(function (obj) {
      if (obj.status === 200) {
        commit(SET_TOKEN, obj.body.token)
      } else {
        commit(CLEAR_FIRST_NAME)
        commit(CLEAR_TOKEN)
      }
      return obj
    }).then(function (obj) {
      dispatch('checkToken')
      // !!!window.location.reload(true)
      return obj
    }).catch(console.error.bind(console))
  },
  // inspect roken
  inspectToken ({dispatch, commit, getters}) {
    const token = getters.TOKEN
    if (token) {
      const decoded = jwtDecode(token)
      const exp = decoded.exp
      const origIssueAt = decoded.orig_iat
      if (exp - (Date.now() / 1000) < 1800 && (Date.now() / 1000) - origIssueAt < 628200) {
        dispatch('refreshToken')
      } else if ((Date.now() / 1000) - origIssueAt < 628200) {
        // DO NOTHING, DO NOT REFRESH
      } else {
        commit(CLEAR_FIRST_NAME)
        commit(CLEAR_TOKEN)
        // PROMPT USER TO RE-LOGIN, THIS ELSE CLAUSE COVERS THE CONDITION WHERE A TOKEN IS EXPIRED AS WELL
      }
    }
  }
}

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
})
