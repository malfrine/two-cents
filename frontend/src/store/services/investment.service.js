import { authHeader } from '@/api/auth-header'

export const investmentService = {
  getUserInvestments
}

function getUserInvestments (userId) {
  const requestOptions = {
    method: 'GET',
    headers: authHeader(),
    body: { userId }
  }

  return fetch('fake-backend/users/investments', requestOptions).then(handleResponse)
}
