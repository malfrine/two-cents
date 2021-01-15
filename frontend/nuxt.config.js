import colors from 'vuetify/es5/util/colors'

export default {
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    titleTemplate: 'Two Cents || %s',
    title: 'Two Cents',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/app/favicon.ico' }
    ],
    script: [
    ]
  },

  server: {
    port: process.env.NUXT_PORT || 8000, // default: 3000
    host: process.env.NUXT_HOST || '0.0.0.0' // default: localhost
  },

  loading: {
    color: '#25b245',
    height: '5px'
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [
  ],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    '~/plugins/axios.js',
    { src: '~/plugins/vue-toastification.js', mode: 'client' }
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify'
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    'vue-toastification/nuxt'
  ],

  // Axios module configuration (https://go.nuxtjs.devThe Same Origin Policy disallows reading the remote resource at/config-axios)
  axios: {
    baseUrl: 'http://localhost:8000'
  },

  publicRuntimeConfig: {
    axios: {
      browserBaseURL: process.env.AXIOS_BASE_URL
    }
  },

  privateRuntimeConfig: {
    axios: {
      baseURL: process.env.AXIOS_BASE_URL
    }
  },

  // Vuetify module configuration (https://go.nuxtjs.dev/config-vuetify)
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: '#25b245',
          accent: colors.blue.darken1,
          secondary: colors.grey.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        },
        light: {
          primary: '#25b245',
          accent: colors.blue.darken1,
          secondary: colors.blueGrey.lighten5,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },

  // toast: {
  //   position: 'top-center',
  //   keepOnHover: true,
  //   duration: 3000,
  //   register: [ // Register custom toasts
  //     {
  //       name: 'my-error',
  //       message: 'Oops...Something went wrong',
  //       options: {
  //         type: 'error'
  //       }
  //     }
  //   ]
  // },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    vendo: ['~/assets/plan-utils.js']
  }
}