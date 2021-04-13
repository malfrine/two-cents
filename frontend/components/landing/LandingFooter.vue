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
          >
            <v-icon size="24px">
              {{ icon.iconName }}
            </v-icon>
          </v-btn>
        </v-card-text>

        <v-divider />

        <v-card-text class="white--text">
          {{ new Date().getFullYear() }} — <strong>Two Cents</strong>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-footer>
</template>

<script>
export default {
  data: () => ({
    icons: [
      {
        iconName: 'mdi-twitter',
        link: 'https://twitter.com/TwoCents_Canada'
      },
      {
        iconName: 'mdi-linkedin',
        link: 'https://www.linkedin.com/company/two-cents-canada'
      }
    ]
  })
}
</script>
