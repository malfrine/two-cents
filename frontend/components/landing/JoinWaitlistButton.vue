<template>
  <v-btn
    color="primary"
    x-large
    rounded
    elevation="4"
    to="/waitlist/join"
    @click="$fire.analytics.logEvent('join_waitlist_page')"
  >
    Join Waitlist
  </v-btn>
</template>
