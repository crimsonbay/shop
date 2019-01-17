// import { CLEAR_FIRST_NAME, CLEAR_TOKEN } from './store/mutation-types'
// let jwtDecode = require('jwt-decode')

// const serverIP = 'localhost'
// const serverPort = '8000'
// export const serverAddr = 'http://' + serverIP + ':' + serverPort
export const serverAddr = ''
export const searchLimit = 20
export const ALLOW_ANON_ORDERS = true
// const OK = 'OK'
// const REFRESH = 'REFRESH'
// const RE_LOGIN = 'RE-LOGIN'

// Add user
export function fetchAddUser (login, name, password) {
  return fetch(serverAddr + '/api/add-user/', {
    method: 'POST',
    mode: 'cors',
    body: JSON.stringify({
      'username': login,
      'first_name': name,
      'password': password })
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// check token, if ok returns user first name
export function fetchCheckToken (token) {
  return fetch(serverAddr + '/api/check-token/', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': ' JWT ' + token
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// obtain JWT by user name and password
export function fetchObtainToken (username, password) {
  return fetch(serverAddr + '/auth/obtain_token/', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'username': username,
      'password': password })
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// refresh token, if ok returns new token
export function fetchRefreshToken (token) {
  return fetch(serverAddr + '/auth/refresh_token/', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'token': token })
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// get main categories for menu
export function fetchGetMenu () {
  return fetch(serverAddr + '/api/get-menu/', {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// returns all categories without parent, the base categories
// witch main children with count of products in children and sub-children
export function fetchGetCategoryOverview () {
  return fetch(serverAddr + '/api/category/', {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// returns category witch children with little image for them
// and with path field - ancestors(name+slug)
export function fetchGetCategory (myCategory) {
  return fetch(serverAddr + '/api/category/' + myCategory, {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// returns all products that have the same category
// or it's subcategory, category takes like the simbols after last slash in path
// optional parameter sort can sort by price or reverse price
export function fetchGetProducts (myCategory, page, sort) {
  return fetch(serverAddr + '/api/product/' + myCategory +
    '?page=' + page + sort, {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// returns products from cart in body
export function fetchGetCartProducts (token, cart) {
  return fetch(serverAddr + '/api/cart/', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    },
    body: cart
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// only for authenticated users, looking for last order,
// if find return it's address name and other delivery info
export function fetchGetLastAddress (token) {
  return fetch(serverAddr + '/api/get-last-addr/', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': ' JWT ' + token
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// create order, if there is not enough products on stock
// it would be in data['error'] by each product
export function fetchCreateOrder (token, data) {
  return fetch(serverAddr + '/api/create-order/', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'// ,
      // 'Authorization': ' JWT ' + token
    },
    body: data
  })
    .then(r => r.json().then(data => ({status: r.status, body: data})))
    .catch(console.error.bind(console))
}

// elasticsearch product
export function fetchSearchProducts (searchQuery, page) {
  let offset = (page - 1) * searchLimit
  return fetch(serverAddr + '/api/list?limit=' + searchLimit +
    '&offset=' + offset + '&search=' + searchQuery, {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// verifies user by uuid if found and return HTTP_200_OK
// user becomes active, uuid changes too
// else return error in data and HTTP_400_BAD_REQUEST
export function fetchVerifyUser (uuid) {
  return fetch(serverAddr + '/api/verify-user?uuid=' + uuid, {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// verifies order by uuid if found and return HTTP_200_OK
// order becomes 'REQUIRES_ATTENTION', uuid changes too
// else return error in data and HTTP_400_BAD_REQUEST
export function fetchVerifyOrder (uuid) {
  return fetch(serverAddr + '/api/verify-user?uuid=' + uuid, {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}

// get product by slug
export function fetchGetProductView (slug) {
  return fetch(serverAddr + '/api/p/' + slug + '/', {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(r => r.json()
      .then(data => ({ status: r.status, body: data })))
    .catch(console.error.bind(console))
}
