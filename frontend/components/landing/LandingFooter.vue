<template>
  <v-footer
    dark
    class="pa-0"
  >
    <v-flex grow>
      <v-card
        flat
        tile
        class="white--text text-center"
      >
        <v-card-text>
          <v-btn
            v-for="(icon, index) in icons"
            :key="index"
            class="mx-4 white--text"
            icon
            :href="icon.link"
            target="_blank"
            @click="$fire.analytics.logEvent('social_media_exploration')"
          >
            <v-icon size="24px">
              {{ icon.iconName }}
            </v-icon>
          </v-btn>
        </v-card-text>

        <v-divider />
        <v-row justify="space-between">
          <v-col cols="12" md="6">
            <v-row justify="start" no-gutters>
              <v-spacer v-if="$vuetify.breakpoint.smAndDown" />
              <TOSDialog />
              |
              <PrivacyPolicyDialog />
              <v-spacer />
            </v-row>
          </v-col>
          <v-col cols="12" md="3">
            {{ new Date().getFullYear() }} — <strong>Two Cents</strong>
          </v-col>
        </v-row>
      </v-card>
    </v-flex>
  </v-footer>
</template>

<script>
import TOSDialog from '@/components/base/TOSDialog.vue'
import PrivacyPolicyDialog from '@/components/base/PrivacyPolicyDialog.vue'

export default {
  components: {
    TOSDialog,
    PrivacyPolicyDialog
  },
  data: () => ({
    icons: [
      {
        iconName: 'mdi-twitter',
        link: 'https://twitter.com/TwoCents_Canada'
      },
      {
        iconName: 'mdi-linkedin',
        link: 'https://www.linkedin.com/company/two-cents-canada'
      },
      {
        iconName: 'mdi-instagram',
        link: 'https://www.instagram.com/twocents_ca/'
      }
    ]
  })
}
</script>
