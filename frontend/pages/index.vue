<template>
  <div>
    <v-row justify="center" align="center" class="mt-5">
      <v-col cols="11">
        <BigLogo class="mt-6" :max-height="$vuetify.breakpoint.mobile ? '70' : '110'" />
      </v-col>
    </v-row>
    <v-row justify="center" align="center" class="mt-n4">
      <v-col cols="11" lg="9" align-self="center">
        <div class="font-weight-medium text-center text-h5 text-md-h4">
          DIY financial planning powered by AI
        </div>
      </v-col>
    </v-row>
    <v-row align="center" justify="center" class="mt-8 mb-7">
      <JoinWaitlistButton />
    </v-row>
    <v-row align="center" justify="center" class="mt-6 mb-4">
      <v-col>
        <DashboardExample max-height="800" />
      </v-col>
    </v-row>

    <v-row dark justify="center" align="center" class="mt-13 mb-n10 pt-8 pb-15" style="background: #212121">
      <v-container class="pa-3">
        <v-row justify="center" class="mb-3">
          <v-col cols="11">
            <div class="text-center text-h4 text-sm-h4 text-md-h3 my-2 white--text">
              A game changing approach to <br class="mb-3">
              <client-only>
                <vue-typer
                  :text="['investments', 'debt', 'taxes', 'retirement', 'financial goals', 'financial planning']"
                  :repeat="Infinity"
                  :shuffle="false"
                  initial-action="typing"
                  :pre-type-delay="70"
                  :type-delay="70"
                  :pre-erase-delay="2000"
                  :erase-delay="20"
                  erase-style="backspace"
                  :erase-on-complete="false"
                  caret-animation="blink"
                />
              </client-only>
            </div>
          </v-col>
        </v-row>
        <v-row justify="center" class="pa-3">
          <div class="text-center text-body-1 white--text mb-10 pa-3">
            We generate a monthly spending plan for you using algorithms that optimize your complete financial picture
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
    <v-container>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="6">
          <div class="text-center text-sm-left text-h4 my-3">
            Financial planning
            <span class="blue--text font-weight-bold">
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
    <!-- <v-container>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="6" :order="$vuetify.breakpoint.xsOnly ? 1 : 0">
          <SuccessFactorsSvg />
        </v-col>
        <v-col cols="12" sm="6" :order="$vuetify.breakpoint.xsOnly ? 0 : 1">
          <div class="text-center text-sm-left text-h4 my-3">
            At last, a plan you can
            <span class="pink--text font-weight-bold">
              trust
            </span>
          </div>
          <div class="text-center text-sm-left text-body-1">
            Two Cents is on your side. We don't broker products and we don't sell your information. You can always rest assured that our recommendations are in your best interests.
          </div>
        </v-col>
      </v-row>
    </v-container> -->
    <v-container>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="6" :order="$vuetify.breakpoint.xsOnly ? 1 : 0">
          <v-sheet dark class="pa-10">
            <v-sheet outlined light class="pa-2">
              <PersonalGoalsSvg />
            </v-sheet>
          </v-sheet>
        </v-col>
        <v-col cols="12" sm="6" :order="$vuetify.breakpoint.xsOnly ? 0 : 1">
          <div class="text-center text-sm-left text-h4 my-3">
            A plan built just
            <span class="purple--text font-weight-bold">
              for you
            </span>
          </div>
          <div class="text-center text-sm-left text-body-1">
            You are unique so your financial plan should be unique too. Our AI builds a bespoke plan based on your loans, investments, and financial goals while accounting for your risk tolerance and spending habits.
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-spacer style="height: 5vh" />
    <v-row class="pa-3" justify="center">
      <div class="text-center text-h4 primary--text mt-15 pa-3">
        Get a head start on your financial planning journey!
      </div>
    </v-row>
    <v-row justify="center" align="center" class="mt-3">
      <JoinWaitlistButton />
    </v-row>
    <v-spacer style="height: 10vh" />
  </div>
</template>

<script>
import MakeItRainSvg from '@/components/landing/MakeItRainSvg.vue'
import PersonalGoalsSvg from '@/components/landing/PersonalGoalsSvg.vue'
// import SuccessFactorsSvg from '@/components/landing/SuccessFactorsSvg.vue'
import FeaturePointCard from '@/components/landing/FeaturePointCard.vue'
import BigLogo from '@/components/logo/BigLogo.vue'
import DashboardExample from '@/components/landing/DashboardExample.vue'
import JoinWaitlistButton from '@/components/landing/JoinWaitlistButton.vue'

export default {
  layout: 'landing',
  components: {
    MakeItRainSvg,
    PersonalGoalsSvg,
    // SuccessFactorsSvg,
    DashboardExample,
    BigLogo,
    FeaturePointCard,
    JoinWaitlistButton
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

<style>

.vue-typer .custom.char {
  color: #25b245;
  font-weight: bold;
}

.vue-typer .custom.caret {
  background-color: #ffffff;
}
</style>
