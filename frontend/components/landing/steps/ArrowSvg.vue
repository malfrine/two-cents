<template>
  <v-hover
    v-slot="{ hover }"
  >
    <svg width="209" height="252" viewBox="0 0 209 252" fill="none" xmlns="http://www.w3.org/2000/svg">

      <path d="M207.423 122.9l-48.9-118c-1.2-3-4.2-4.9-7.4-4.9H8.023c-5.7 0-9.6 5.8-7.4 11.1l47.6 114.9-47.6 114.9c-2.2 5.3 1.7 11.1 7.4 11.1h143.1c3.2 0 6.2-1.9 7.4-4.9l48.9-118c.8-2 .8-4.2 0-6.2z" fill="#25b245" />
      <path d="M207.423 122.9l-47.2-114c-1.2-3-4.2-4.9-7.4-4.9H9.723c-5.7 0-9.6 5.8-7.4 11.1l46 110.9-47.7 114.9c-2.2 5.3 1.7 11.1 7.4 11.1h143.1c3.2 0 6.2-1.9 7.4-4.9l48.9-118c.8-2 .8-4.2 0-6.2z" fill="#171717" />

      <text x="91" y="50" text-anchor="middle" :fill="`${hover ? 'white': 'grey'}`">{{ text }}</text>
      <image x="85" y="90" :href="image" height="75" width="75" />

    </svg>
  </v-hover>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true
    },
    image: {
      type: String,
      required: true
    }
  }
}
</script>
