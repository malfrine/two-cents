// import { authHeader } from '@/services/auth-header-helper.js'

export const authService = {
  login,
  logout
}

function handleResponse (response) {
  console.log(response.text())
  return response.text().then(text => {
    console.log(response)
    const data = text && JSON.parse(text)
    if (!response.ok) {
      if (response.status === 401) {
        // auto logout if 401 response returned from api
        logout()
        location.reload(true)
      }

      const error = (data && data.message) || response.statusText
      return Promise.reject(error)
    }

    return data
  })
}

function login (username, password) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  }
  return fetch('facke-backend-url/users/authenticate', requestOptions)
    .then(handleResponse)
    .then(
      user => {
        console.log('sucessful login')
        // login successful if there's a jwt token in the response
        if (user.token) {
        // store user details and jwt token in local storage to keep user logged in between page refreshes
          localStorage.setItem('user', JSON.stringify(user))
        }
        return user
      })
}
function logout () {
  // remove user from local storage to log user out
  localStorage.removeItem('user')
}
