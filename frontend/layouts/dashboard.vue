<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :expand-on-hover="!$vuetify.breakpoint.mobile"
      app
      dark
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      fixed
      app
      dark
    >
      <v-app-bar-nav-icon v-if="!drawer" @click.stop="drawer = !drawer; miniVariant=false" />
      <v-spacer />
      <div class="d-flex justify-center">
        <v-img
          max-width="150"
          max-height="75"
          src="/logo-white.png"
        />
      </div>
      <v-spacer />
      <v-btn icon @click.prevent="$vuetify.theme.isDark = !$vuetify.theme.isDark">
        <v-icon>mdi-theme-light-dark</v-icon>
      </v-btn>
      <v-btn
        icon
        @click.stop="onLogoutClick"
      >
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <nuxt />
      </v-container>
    </v-main>
    <BaseFooter />
  </v-app>
</template>

<script>
import BaseFooter from '@/components/base/BaseFooter'

export default {
  components: {
    BaseFooter
  },
  data () {
    return {
      drawer: true,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Welcome',
          to: '/'
        },
        {
          icon: 'mdi-badge-account-horizontal-outline',
          title: 'Profile',
          to: '/dashboard/profile'
        },
        {
          icon: 'mdi-finance',
          title: 'Plan',
          to: '/dashboard/plan'
        }
      ],
      miniVariant: false
    }
  },
  methods: {
    onLogoutClick () {
      this.$store.dispatch('auth/postLogout')
      this.$store.dispatch('finances/resetUserFinances')
      this.$router.push('/')
    }
  }
}
</script>
