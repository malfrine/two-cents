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
            v-for="icon in icons"
            :key="icon"
            class="mx-4 white--text"
            icon
          >
            <v-icon size="24px">
              {{ icon }}
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
      'mdi-twitter',
      'mdi-linkedin',
      'mdi-instagram'
    ]
  })
}
</script>
