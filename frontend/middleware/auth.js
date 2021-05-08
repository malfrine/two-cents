export default function ({ store, redirect }) {
  // If the user is not authenticated
  if (!store.getters['firebase-auth/isLoggedIn']) {
    return redirect('/login')
  }
}
