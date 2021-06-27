<template>
  <v-footer
    :app="app"
    dark
    class="pa-0"
  >
    <v-flex grow>
      <v-card
        flat
        tile
        class="white--text text-center px-4"
      >
        <v-card-text v-if="showSocialLinks">
          <v-btn
            v-for="(icon, index) in icons"
            :key="index"
            class="mx-4 white--text"
            icon
            :href="icon.link"
            rel="noreferrer"
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
          <v-col cols="12" md="6" class="d-flex justify-center justify-md-start">
            <v-row no-gutters class="d-flex justify-center justify-md-start">
              <TOSDialog class="mr-2" />
              |
              <PrivacyPolicyDialog class="ml-2" />
            </v-row>
          </v-col>
          <v-col cols="12" md="6" class="d-flex justify-center justify-md-end">
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
  props: {
    showSocialLinks: {
      type: Boolean,
      default: true
    },
    app: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    icons: [
      {
        iconName: 'mdi-twitter',
        link: 'https://twitter.com/TwoCents_CA'
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
