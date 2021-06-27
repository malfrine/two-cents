import colors from 'vuetify/es5/util/colors'
import { makeSeoHeaders } from './assets/utils.js'

const isDev = process.env.NODE_ENV === 'development'
let firebaseConfig
let domain
if (isDev) {
  console.log('Currently operating in development mode')
  firebaseConfig = {
    apiKey: 'AIzaSyDXd2TsrIQ2wiwiDsS_Z3dTtakdVH8EJEE',
    authDomain: 'two-cents-canada-dev.firebaseapp.com',
    projectId: 'two-cents-canada-dev',
    storageBucket: 'two-cents-canada-dev.appspot.com',
    messagingSenderId: '479438313062',
    appId: '1:479438313062:web:fcc309df61d45908aa3fa7',
    measurementId: 'G-N7E647R6C5'
  }
  domain = 'http://localhost:8000'
} else {
  console.log('Currently operating in production mode')
  firebaseConfig = {
    apiKey: 'AIzaSyAPb1qWmgQ3tFpLAqRUf2Bshqf4FdlwfKE',
    authDomain: 'two-cents-canada.firebaseapp.com',
    projectId: 'two-cents-canada',
    storageBucket: 'two-cents-canada.appspot.com',
    messagingSenderId: '471669331840',
    appId: '1:471669331840:web:93ef3e302b6a0257289365',
    measurementId: 'G-F876X8NTHY'
  }
  domain = 'https://two-cents.ca'
}

export default {
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    titleTemplate: 'Two Cents || %s',
    title: 'Two Cents',
    htmlAttrs: {
      lang: 'en',
      amp: true
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'DIY financial planning powered by AI' },
      ...makeSeoHeaders()
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/app/favicon.ico' },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400&display=swap'
      },
      {
        rel: 'link',
        href: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1622266448/two-cents-dashboard-v1_hrulw1.png'
      }
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
    '~/plugins/instrument-colors.js',
    { src: '~/plugins/vue-toastification.js', mode: 'client' },
    { src: '~/plugins/typed.js', mode: 'client' }
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
    'vue-toastification/nuxt',
    '@nuxtjs/firebase',
    'nuxt-user-agent',
    '@nuxtjs/sentry'

  ],

  firebase: {
    config: firebaseConfig,
    onFirebaseHosting: false,
    services: {
      auth: {
        initialize: {
          onAuthStateChangedAction: 'firebase-auth/onAuthStateChanged'
        },
        ssr: true,
        emulatorPort: null
      },
      performance: true,
      analytics: true
    }
  },

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

  env: {
    baseUrl: domain
  },

  sentry: {
    dsn: process.env.SENTRY_DSN || ''
  },

  // Vuetify module configuration (https://go.nuxtjs.dev/config-vuetify)
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    treeShake: true,
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
