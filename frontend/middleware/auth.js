export default function ({ store, redirect, route }) {
  // If the user is not authenticated
  if (!store.getters['firebase-auth/isLoggedIn']) {
    return redirect({ name: 'login' })
  }
}
