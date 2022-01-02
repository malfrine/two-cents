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
      <v-btn icon @click.prevent="$vuetify.theme.isDark = !$vuetify.theme.isDark">
        <v-icon>mdi-theme-light-dark</v-icon>
      </v-btn>
      <v-spacer />
      <div class="d-flex justify-center">
        <NuxtLink to="/">
          <SmallLogo />
        </NuxtLink>
      </div>
      <v-spacer />

      <v-btn
        large
        color="primary"
        class="mx-1"
        @click="openRegistrationPrompt"
      >
        Try For Free
      </v-btn>
      <PublishedPlanRegistrationDialog
        :show-dialog="showRegistrationPrompt"
        :published-plan-id="publishedPlanId"
        @close="closeRegistrationPrompt"
      />
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
import PublishedPlanRegistrationDialog from '@/components/plan/PublishedPlanRegistrationDialog.vue'

export default {
  components: {
    SmallLogo,
    PublishedPlanRegistrationDialog
  },
  data () {
    return {
      showRegistrationPrompt: false,
      drawer: true,
      miniVariant: false,
      items: [
        {
          icon: 'mdi-badge-account-horizontal-outline',
          title: 'Profile',
          to: 'profile'
        },
        {
          icon: 'mdi-finance',
          title: 'Plan',
          to: 'plan'
        }
      ]
    }
  },
  computed: {
    publishedPlanId () {
      return Number(this.$route.params.id)
    },
    planExists () {
      return this.$store.getters['published_plans/getPublishedPlanExists'](this.publishedPlanId)
    }
  },
  methods: {
    openRegistrationPrompt () {
      this.showRegistrationPrompt = true
    },
    closeRegistrationPrompt () {
      this.showRegistrationPrompt = false
    }
  }
}
</script>
