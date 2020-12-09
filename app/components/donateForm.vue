<template>
    <div>
        <v-container>
            <v-row align="center">
                <v-btn-toggle v-model="amount" borderless>
                    <v-btn value="price_1HdsGvKh5bC1GE0OttvpArCC">
                        <span>$5</span>
                    </v-btn>

                    <v-btn value="price_1HdsGvKh5bC1GE0O7dYxJfRK">
                        <span>$10</span>
                    </v-btn>

                    <v-btn value="price_1HdrppKh5bC1GE0OqLRYJ8Da">
                        <span>$20</span>
                    </v-btn>

                    <v-btn value="price_1HdsGvKh5bC1GE0OMOxtpK1Q">
                        <span>$50</span>
                    </v-btn>
                </v-btn-toggle>
            </v-row>
            <v-row class="mt-1">
                <h3 class="mr-4 ml-1">Choose Payment</h3>
                <v-icon>mdi-lock</v-icon>
                <div class="mt-1">SECURE</div>
            </v-row>
            <v-row class="mt-1">
                <stripe-checkout
                    ref="checkoutRef"
                    :pk="publishableKey"
                    :lineItems="lineItems()"
                    :submitType="submitType"
                    :mode="mode"
                    :successUrl="successUrl"
                    :cancelUrl="cancelUrl"
                >
                    <template slot="checkout-button">
                        <v-btn x-large @click="checkout" class="success px-15">
                            <v-icon medium class="pr-2">mdi-contactless-payment</v-icon>
                            <span>Stripe</span>
                        </v-btn>
                    </template>
                </stripe-checkout>
            </v-row>
            <v-snackbar v-model="snackbar" :timeout="timeout" :color="snackColor">
                {{ text }}

                <template v-slot:action="{ attrs }">
                    <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
                        Close
                    </v-btn>
                </template>
            </v-snackbar>
        </v-container>
    </div>
</template>

<script>
export default {
    data() {
        return {
            amount: "price_1HdsGvKh5bC1GE0OttvpArCC",
            mode: "payment",
            loading: false,
            publishableKey: process.env.STRIPE_PK,
            submitType: "donate",
            successUrl: "http://localhost:3000/app/donate?test=success",
            cancelUrl: "http://localhost:3000/app/donate?test=fail",
            snackbar: false,
            text: "Thank you for your donation! 🥰",
            timeout: 5000,
            snackColor: "success",
        };
    },
    methods: {
        checkout() {
            this.$refs.checkoutRef.redirectToCheckout();
        },
        lineItems() {
            return [{ price: this.amount, quantity: 1 }];
        },
    },
    mounted() {
        if (this.$route.query.test == "success") {
            this.snackbar = true;
        } else if (this.$route.query.test == "fail") {
            this.snackbar = true;
            this.text = "Oh no, your donation did not went through! 😔";
            this.snackColor = "error";
        }
    },
};
</script>

<style></style>
