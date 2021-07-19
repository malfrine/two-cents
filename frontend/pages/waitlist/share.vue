<template>
  <v-container fill-height>
    <v-row justify="center">
      <v-col cols="12" md="7" lg="6">
        <v-card min-height="500" elevation="10" align="center">
          <v-container>
            <v-row justify="center" class="my-3">
              <NuxtLink to="/">
                <BigLogo max-height="35" />
              </NuxtLink>
            </v-row>
            <div class="text-h5 text-md-h4">
              Tell your friends
            </div>
            <v-card-subtitle>
              Share your referral link with your friends and we'll bump you up the queue
            </v-card-subtitle>
            <v-divider class="mt-2 mb-10" />

            <v-row justify="center" class="my-5">
              <v-btn
                v-for="(icon, index) in iconsToDisplay"
                :key="index"
                fab
                :color="icon.color"
                :href="icon.link"
                target="_blank"
                class="ma-3"
                @click="$fire.analytics.logEvent('share_waitlist')"
              >
                <v-icon size="24px" color="white">
                  {{ icon.iconName }}
                </v-icon>
              </v-btn>
            </v-row>
            <v-row justify="center" align="center" class="mt-10">
              <v-col cols="11" md="8">
                <v-row justify="center" align="center">
                  <v-text-field
                    v-model="referralLink"
                    disabled
                    filled
                    outlined
                  >
                    <template v-slot:append />
                  </v-text-field>
                  <v-btn
                    depressed
                    tile
                    dark
                    fab
                    style="margin-bottom: 30px;"
                    class="ml-n1"
                    @click.prevent="copyText"
                  >
                    <v-icon>
                      {{ isShowCopiedConfirmation ? "mdi-check" : "mdi-clipboard" }}
                    </v-icon>
                  </v-btn>
                </v-row>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import BigLogo from '@/components/logo/BigLogo'
import { delay, copyToClipboard } from '~/assets/utils.js'

export default {
  layout: 'landing',
  components: {
    BigLogo
  },
  data () {
    const referralCode = this.$store.state.waitlist.referralCode || ''

    const smsArgumentDelimiter = this.$ua.isFromIos() ? '&' : '?'

    let linkQuery
    if (referralCode) {
      linkQuery = `/?referralCode=${referralCode}`
    } else {
      linkQuery = ''
    }
    const url = `${process.env.baseUrl}${linkQuery}`
    const title = 'Join the Two Cents waitlist to build free AI powered financial plan!'
    const hashtags = 'PersonalFinance,finance,AI'

    return {
      referralLink: url,
      isShowCopiedConfirmation: false,
      mobileOnlyIcons: [
        {
          iconName: 'mdi-cellphone',
          link: encodeURI(`sms:${smsArgumentDelimiter}body=${url}${title}`),
          color: '#131418',
          mobileOnly: true
        },
        {
          iconName: 'mdi-whatsapp',
          link: encodeURI(`https://api.whatsapp.com/send?&text=${title}%20${url}`),
          color: '#25D366',
          mobileOnly: true
        }
      ],
      allDevicIcons: [
        {
          iconName: 'mdi-facebook',
          link: encodeURI(`https://www.facebook.com/sharer.php?u=${url}`),
          color: '#3b5998',
          mobileOnly: false
        },
        {
          iconName: 'mdi-twitter',
          link: encodeURI(`https://twitter.com/intent/tweet?url=${url}&text=${title}&via=&hashtags=${hashtags}`),
          color: '#55acee',
          mobileOnly: false
        },
        {
          iconName: 'mdi-linkedin',
          link: encodeURI(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`), // TODO: fix this one
          color: '#0077B5',
          mobileOnly: false
        },
        {
          iconName: 'mdi-email',
          link: encodeURI(`mailto:?subject=${title}&body=${url} ${title}`),
          color: '#131418',
          mobileOnly: false
        }
      ]
    }
  },
  computed: {
    iconsToDisplay () {
      if (this.$vuetify.breakpoint.mobile) {
        return [...this.mobileOnlyIcons, ...this.allDevicIcons]
      } else {
        return this.allDevicIcons
      }
    }
  },
  methods: {
    async copyText () {
      this.$fire.analytics.logEvent('share_waitlist')
      copyToClipboard(this.referralLink)
      this.isShowCopiedConfirmation = true
      await delay(2500)
      this.isShowCopiedConfirmation = false
    }
  },
  head () {
    return {
      title: 'Waitlist'
    }
  }
}
</script>
