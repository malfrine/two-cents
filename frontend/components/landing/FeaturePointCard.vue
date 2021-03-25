<template>
  <v-hover v-slot="{ hover }">
    <v-card color="blue-grey lighten-5" :elevation="hover ? 4 : 1">
      <v-card-title>
        <v-icon large color="primary" class="mr-3">
          {{ iconName }}
        </v-icon>
        {{ title }}
      </v-card-title>
      <v-divider />
      <v-card-subtitle>
        {{ text }}
      </v-card-subtitle>
    </v-card>
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
