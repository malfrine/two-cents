<template>
  <v-app>
    <v-navigation-drawer
      v-if="$vuetify.breakpoint.mobile"
      v-model="drawer"
      right
      app
      dark
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items.slice().reverse()"
          :key="i"
          :to="item.to"
          :href="item.href"
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
      :hide-on-scroll="!$vuetify.breakpoint.mobile"
      app
      dark
      flat
      style="background: #121212"
    >
      <div class="d-flex justify-center align-center">
        <NuxtLink to="/">
          <SmallLogo />
        </NuxtLink>
      </div>
      <v-spacer />
      <v-app-bar-nav-icon v-if="$vuetify.breakpoint.mobile" @click.stop="drawer = !drawer" />
      <div v-else>
        <v-btn
          v-for="(item, i) in items"
          :key="i"
          :href="item.href"
          :to="item.to"
          :outlined="item.outlined"
          :text="item.text"
          :large="item.large"
          color="primary"
          nuxt
          class="mx-1"
        >
          {{ item.title }}
        </v-btn>
      </div>
    </v-app-bar>
    <v-main>
      <nuxt />
    </v-main>
    <BaseFooter />
  </v-app>
</template>

<script>
import BaseFooter from '@/components/base/BaseFooter.vue'
import SmallLogo from '@/components/logo/SmallLogo.vue'

export default {
  components: {
    BaseFooter,
    SmallLogo
  },
  data () {
    return {
      drawer: false,
      items: [
        {
          icon: 'mdi-lightbulb-outline',
          title: 'Blog',
          href: 'https://blog.two-cents.ca',
          outlined: false,
          text: true
        },
        {
          icon: 'mdi-login',
          title: 'Login',
          to: '/login',
          outlined: true,
          large: true,
          text: false
        },
        {
          icon: 'mdi-account',
          title: 'Register',
          to: '/onboard',
          outlined: false,
          large: true,
          text: false
        }

      ]
    }
  },
  created () {
    this.$vuetify.theme.isDark = true
  }
}
</script>
