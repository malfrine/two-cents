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
      <v-divider class="my-3" />
      <v-list>
        <v-list-item
          v-for="(item, i) in bottomItems"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }} </v-icon>
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
        <NuxtLink to="/">
          <SmallLogo />
        </NuxtLink>
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
    <BaseFooter :show-social-links="false" :app="true" />
  </v-app>
</template>

<script>
import SmallLogo from '@/components/logo/SmallLogo.vue'

export default {
  components: {
    SmallLogo
  },
  data () {
    return {
      drawer: true,
      items: [
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
      bottomItems: [
        {
          icon: 'mdi-wrench',
          title: 'Settings',
          to: '/dashboard/settings'
        }
      ],
      miniVariant: false
    }
  },
  created () {
    this.$store.dispatch('enums/getAllEnums')
  },
  methods: {
    onLogoutClick () {
      this.$router.push('/')

      this.$fire.auth.signOut()
      this.$store.dispatch('plan/resetPlans')

      this.$store.dispatch('finances/resetUserFinances')
    }
  }
}
</script>
