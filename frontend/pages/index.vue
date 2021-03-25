<template>
  <div>
    <div style="height: 100vh;">
      <v-row justify="center">
        <v-col cols="12" lg="9">
          <BigLogoSvg />
          <div class="primary--text text-center text-h6 text-sm-h4 text-xl-h3">
            DIY financial planning powered by AI
          </div>
        </v-col>
      </v-row>
      <v-container class="px-10">
        <v-row>
          <v-col cols="12" sm="6">
            <div class="text-center">
              DASHBOARD IMAGE HERE
            </div>
          </v-col>
          <v-col cols="12" sm="6">
            <RequestAccessButton />
          </v-col>
        </v-row>
      </v-container>
    </div>
    <v-container>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="6">
          <div class="text-center text-sm-left text-h4 my-3">
            Financial planning
            <span class="blue--text">
              without the fees
            </span>
          </div>
          <div class="text-center text-sm-left text-body-1">
            Everyone deserves a financial plan. Build a free financial plan today in under 15 minutes!
          </div>
        </v-col>
        <v-col cols="12" sm="6">
          <MakeItRainSvg />
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="6" :order="$vuetify.breakpoint.xsOnly ? 1 : 0">
          <SuccessFactorsSvg />
        </v-col>
        <v-col cols="12" sm="6" :order="$vuetify.breakpoint.xsOnly ? 0 : 1">
          <div class="text-center text-sm-left text-h4 my-3">
            At last, a plan you can
            <span class="pink--text">
              trust
            </span>
          </div>
          <div class="text-center text-sm-left text-body-1">
            Two Cents is on your side. We don't broker products and we don't sell your information. You can always rest assured that our recommendations are in your best interests.
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="6">
          <div class="text-center text-sm-left text-h4 my-3">
            A plan built just
            <span class="purple--text">
              for you
            </span>
          </div>
          <div class="text-center text-sm-left text-body-1">
            You are unique so your financial plan should be unique to you. Our AI builds a bespoke plan based on your loans, investments, and financial goals while accounting for your risk tolerance and spending habits.
          </div>
        </v-col>
        <v-col cols="12" sm="6">
          <v-sheet dark class="pa-10">
            <v-sheet outlined light class="pa-2">
              <PersonalGoalsSvg />
            </v-sheet>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
    <v-spacer style="height: 10vh" />
    <v-row dark justify="center" align="center" class="mt-15 mb-n10 pt-10 pb-15" style="background: #212121">
      <v-container class="px-8">
        <v-row justify="center">
          <div class="text-center text-h4 text-md-h3 my-2 white--text">
            A <span class="primary--text">game-changing</span> approach to financial planning
          </div>
        </v-row>
        <v-row justify="center">
          <div class="text-center text-body-1 white--text">
            We generate a monthly spending plan for you using the same algorithms and computing power used by Wall Street hedge funds
          </div>
        </v-row>
      </v-container>
    </v-row>
    <v-container>
      <v-row class="mt-n8 mb-15">
        <v-col v-for="(featurePoint, index) in featurePoints" :key="index" cols="12" sm="6">
          <FeaturePointCard :icon-name="featurePoint.iconName" :title="featurePoint.title" :text="featurePoint.text" />
        </v-col>
      </v-row>
    </v-container>
    <v-spacer style="height: 5vh" />
    <div class="text-center text-h3 primary--text mt-15">
      Save thousands in just 15 minutes!
    </div>
    <v-row justify="center" align="center" no-gutters class="py-0">
      <v-col cols="6">
        <RequestAccessButton />
      </v-col>
    </v-row>
    <v-spacer style="height: 15vh" />
  </div>
</template>

<script>
import MakeItRainSvg from '@/components/landing/MakeItRainSvg.vue'
import PersonalGoalsSvg from '@/components/landing/PersonalGoalsSvg.vue'
import SuccessFactorsSvg from '@/components/landing/SuccessFactorsSvg.vue'
import FeaturePointCard from '@/components/landing/FeaturePointCard.vue'
import BigLogoSvg from '@/components/logo/BigLogoSvg.vue'
import RequestAccessButton from '@/components/landing/RequestAccessButton.vue'

export default {
  layout: 'landing',
  components: {
    MakeItRainSvg,
    PersonalGoalsSvg,
    SuccessFactorsSvg,
    BigLogoSvg,
    FeaturePointCard,
    RequestAccessButton
  },
  data () {
    return {
      featurePoints: [
        {
          iconName: 'mdi-trophy',
          title: 'Financial Goals',
          text: "Ensure that you can save for a new house, your children's education, or your dream vacation."
        },
        {
          iconName: 'mdi-flag-checkered',
          title: 'Retirement',
          text: "Ensure that you're saving up enough money for retirement based on your expected spending habits"
        },
        {
          iconName: 'mdi-bank',
          title: 'Loans',
          text: 'Strategically pay off loans to minimize money you lose on interest'
        },
        {
          iconName: 'mdi-rocket',
          title: 'Investments',
          text: 'Strategically invest and diversify your portfolio based on your risk tolerance'
        },
        {
          iconName: 'mdi-city',
          title: 'Taxes',
          text: 'Minimize your income taxes by strategically investing in RRSPs (Registered Retirement Savings Plan) and TFSAs (Tax Free Savings Account)'
        },
        {
          iconName: 'mdi-compare',
          title: 'Compare Plans',
          text: 'Compare your Two Cents plan to conventional financial planning methods like the snowball and avalanche method'
        }
      ]
    }
  },
  head () {
    return {
      title: 'Hello, World!'
    }
  }

}
</script>

<style scoped>
  .v-input__append-outer {
    margin: 0 !important
  }
</style>
