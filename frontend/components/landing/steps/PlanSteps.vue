<template>
  <div>
    <v-container>
      <v-card class="pa-5">
        <v-container>
          <div class="font-weight-bold text-h5 text-md-h4 text-center my-5 mb-10 pa-3">
            All it takes is 4 easy steps
          </div>
          <v-row justify="center" class="mx-3">
            <v-slide-group>
              <v-slide-item
                v-for="(step, i) in steps"
                :key="i"
              >
                <ArrowSvg :text="step.text" :image="step.imageLink" />
              </v-slide-item>
            </v-slide-group>
          </v-row>
        </v-container>
        <v-divider class="my-7" />
        <v-row justify="center" align="center">
          <v-col cols="12" md="6" lg="6">
            <v-container :class="`pa-${$vuetify.breakpoint.smAndDown ? 0 : 10}`">
              <StepText
                :title="profile.title"
                :main-text="profile.mainText"
                :learn-more-url="profile.learnMoreUrl"
                :category="profile.category"
                :number="profile.order"
              />
            </v-container>
          </v-col>
          <v-col cols="12" md="6" lg="6">
            <ImageCarousel :image-urls="profile.imageUrls" :gradient-degree="40" />
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col cols="12" md="6" lg="6" :order="$vuetify.breakpoint.smAndDown ? 1 : 0">
            <ImageCarousel :image-urls="goal.imageUrls" :gradient-degree="209" />
          </v-col>
          <v-col cols="12" md="6" lg="6" :order="$vuetify.breakpoint.smAndDown ? 0 : 1">
            <v-container :class="`pa-${$vuetify.breakpoint.smAndDown ? 0 : 10}`">
              <StepText
                :title="goal.title"
                :main-text="goal.mainText"
                :learn-more-url="goal.learnMoreUrl"
                :category="goal.category"
                :number="goal.order"
              />
            </v-container>
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col cols="12" md="6" lg="6">
            <v-container :class="`pa-${$vuetify.breakpoint.smAndDown ? 0 : 10}`">
              <StepText
                :title="loan.title"
                :main-text="loan.mainText"
                :learn-more-url="loan.learnMoreUrl"
                :category="loan.category"
                :number="loan.order"
              />
            </v-container>
          </v-col>
          <v-col cols="12" md="6" lg="6">
            <ImageCarousel :image-urls="loan.imageUrls" :gradient-degree="40" />
          </v-col>
        </v-row>
        <v-row id="test" justify="center" align="center" class="mt-10" style="margin-bottom: -150">
          <v-col cols="12" md="6" lg="6" :order="$vuetify.breakpoint.smAndDown ? 1 : 0">
            <ImageCarousel :image-urls="investment.imageUrls" :gradient-degree="209" />
          </v-col>
          <v-col cols="12" md="6" lg="6" :order="$vuetify.breakpoint.smAndDown ? 0 : 1" style="z-index: 1">
            <v-container :class="`pa-${$vuetify.breakpoint.smAndDown ? 0 : 10}`">
              <StepText
                :title="investment.title"
                :main-text="investment.mainText"
                :learn-more-url="investment.learnMoreUrl"
                :category="investment.category"
                :number="investment.order"
              />
            </v-container>
          </v-col>
        </v-row>
        <Sparkline v-if="$vuetify.breakpoint.mdAndUp" style="margin-top: -250px; z-index: 0" />
      </v-card>
    </v-container>
  </div>
</template>

<script>
import Sparkline from '@/components/landing/steps/Sparkline'
import ImageCarousel from '@/components/landing/steps/ImageCarousel'
import StepText from '@/components/landing/steps/StepText'
import ArrowSvg from '@/components/landing/steps/ArrowSvg'

export default {
  components: {
    Sparkline,
    ImageCarousel,
    StepText,
    ArrowSvg
  },
  data () {
    return {
      steps: [
        {
          text: 'Preferences',
          imageLink: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1622082919/Landing%20Page%20Icons/Preferences-Icon.png'
        },
        {
          text: 'Goals',
          imageLink: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1622082918/Landing%20Page%20Icons/Goals-Icon.png'
        },
        {
          text: 'Loans',
          imageLink: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1622088651/Landing%20Page%20Icons/loans-icon.png'
        },
        {
          text: 'Investments',
          imageLink: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1622082919/Landing%20Page%20Icons/Investments-Icon.png'
        }
      ],
      loan: {
        order: 3,
        category: 'Loans',
        title: 'Add your loans',
        mainText: 'Add your mortgage, student loans, credit cards and more. Choose between fixed and variable interest rates and specify the loan due date. Our AI will make sure you pay off all your loans on time and minimize the amount of money you lose on interest.',
        imageUrls: [
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621811022/steps/loans/student-loan_pqv4dl.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621811462/steps/loans/mortgage_qcf6e7.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621811462/steps/loans/car-loan_kyol2e.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621811462/steps/loans/credit-card-loan_em2m19.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621811462/steps/loans/personal-loan_mahr20.png'
        ]
      },
      investment: {
        order: 4,
        category: 'Investments',
        title: 'Add your investments',
        mainText: 'Add your mutual funds, ETFs, stocks, term deposits and more. Choose between TFSA, RRSP and Non-registered accounts. Our AI will determine how to allocate your funds in order to meet your financial goals and maximize your net worth.',
        imageUrls: [
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621812210/steps/investments/etf-1_ihodzc.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621812210/steps/investments/mutual-fund_mmgn4o.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621812210/steps/investments/etf-2_selkh7.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621812210/steps/investments/cash_faunat.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621812210/steps/investments/term-deposit_uvvluk.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621812210/steps/investments/stock_yhgwbx.png'
        ]
      },
      goal: {
        order: 2,
        category: 'Goals',
        title: 'Tell us your goals',
        mainText: 'Add your financial goals like saving for a big purchase and building up a nest egg. Specify when you would like to reach this goal and our AI will identify the best plan to meet your goals by the due date',
        imageUrls: [
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621810102/steps/goals/nest-egg_wq6xlh.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621810102/steps/goals/big-purchase_zdwi5z.png'
        ]
      },
      profile: {
        order: 1,
        category: 'Preferences',
        title: 'Tell us a little about yourself',
        mainText: 'Add your financial information and preferences so we can build you a bespoke plan.',
        imageUrls: [
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621801886/steps/profile/user-info_sig8i1.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621807327/steps/profile/financial-information_pvpxup.png',
          'https://res.cloudinary.com/two-cents-ca/image/upload/v1621807114/steps/profile/financial-preferences_wrhhd7.png'
        ]
      }
    }
  }
}
</script>
