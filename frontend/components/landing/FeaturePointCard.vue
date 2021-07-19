<template>
  <v-hover v-slot="{ hover }">
    <v-sheet :elevation="hover ? 0 : 0" class="card">
      <v-row>
        <v-col cols="12">
          <v-card-title class="mb-n6">
            <p>
              <v-icon :large="$vuetify.breakpoint.mdAndUp" color="primary" class="mb-2 mr-1">
                {{ iconName }}
              </v-icon>
              {{ title }}
            </p>
          </v-card-title>
        </v-col>
      </v-row>

      <v-divider class="mt-4 mb-2" style="height: 100%" />
      <v-card-subtitle>
        {{ text }}
      </v-card-subtitle>
    </v-sheet>
  </v-hover>
</template>

<script>
export default {
  props: ['text', 'title', 'iconName'],
  data: () => ({
    show: false
  })
}
</script>

<style scoped>
.card {
  background: #121212;
  /* border: 2px solid rgba(37,178,69,1); */
  /* border-image: linear-gradient(60deg, rgba(37,178,69,1) 0%, rgba(53,163,87,1) 7%, rgba(68,148,105,1) 26%, rgba(84,133,124,1) 44%, rgba(100,117,142,1) 66%, rgba(115,102,160,1) 85%) 1 stretch; */
}
</style>
