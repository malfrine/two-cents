<template>
  <div>
    <v-row justify="center" align="center" class="mt-5">
      <v-col cols="11">
        <BigLogo class="mt-6" :max-height="$vuetify.breakpoint.mobile ? '70' : '110'" />
      </v-col>
    </v-row>
    <v-row justify="center" align="center" class="mt-4">
      <v-col cols="11" lg="6" align-self="center">
        <div class="font-weight-bold text-center text-h5 text-md-h4">
          Take your money further
        </div>
        <div class="font-weight-bold text-center grey--text text text-md-h6">
          Use our AI to create a free monthly spending plan that will help you reach your financial goals
        </div>
      </v-col>
    </v-row>
    <v-row justify="center" class="mt-10">
      <JoinWaitlistButton />
    </v-row>
    <!-- <v-container>
      <v-row align="center" justify="center" align-content="space-between" class="mt-8 mb-7">
        <v-col cols="12" md="8">
          <div class="font-weight-medium text-center text-h5 text-md-h4">
            Take your money further
          </div>
          <br>
          <div class="text-center text-h6">
            Use our AI to create a free monthly spending plan that will help you reach your financial goals
          </div>
        </v-col>
        <v-col cols="12" md="4" align-celf="center" class="text-center">
          <JoinWaitlistButton />
        </v-col>
      </v-row>
    </v-container> -->
    <v-row align="center" justify="center" class="mt-6 mb-4">
      <v-col>
        <DashboardExample max-height="800" />
      </v-col>
    </v-row>
    <v-container fluid>
      <v-row justify="center" align="center" class="mt-13 mb-n10 pt-8 pb-15 gradient">
        <v-col class="my-n3">
          <v-row style="background: #121212" class="mt-n7 mb-n14">
            <v-container class="pa-3">
              <v-row justify="center" class="mb-3">
                <v-col cols="11">
                  <div class="text-center text-h4 text-sm-h4 text-md-h3 my-2 white--text">
                    A game changing approach to <br class="mb-3">
                    <client-only>
                      <vue-typer
                        :text="['investments', 'debt', 'taxes', 'retirement', 'financial goals']"
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
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row class="mt-n8 mb-15">
        <v-col v-for="(featurePoint, index) in featurePoints" :key="index" cols="12" sm="6">
          <FeaturePointCard :icon-name="featurePoint.iconName" :title="featurePoint.title" :text="featurePoint.text" />
        </v-col>
      </v-row>
    </v-container>
    <PlanSteps />
    <v-spacer style="height: 5vh" />
    <v-row class="pa-3" justify="center">
      <div class="text-center text-h4 mt-15 pa-3">
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
import FeaturePointCard from '@/components/landing/FeaturePointCard.vue'
import BigLogo from '@/components/logo/BigLogo.vue'
import DashboardExample from '@/components/landing/DashboardExample.vue'
import JoinWaitlistButton from '@/components/landing/JoinWaitlistButton.vue'
import PlanSteps from '@/components/landing/steps/PlanSteps.vue'

export default {
  layout: 'landing',
  components: {
    DashboardExample,
    BigLogo,
    FeaturePointCard,
    JoinWaitlistButton,
    PlanSteps
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
  word-break: break-all;
}

.vue-typer .custom.caret {
  background-color: #ffffff;
}

.gradient {
  background: linear-gradient(60deg, rgba(37,178,69,1) 0%, rgba(53,163,87,1) 7%, rgba(68,148,105,1) 26%, rgba(84,133,124,1) 44%, rgba(100,117,142,1) 66%, rgba(115,102,160,1) 85%);
}
</style>
