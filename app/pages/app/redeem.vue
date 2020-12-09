<template>
    <div>
        <div class="head">
            <v-container>
                <h1 class="indigo--text">You have {{ points }} points</h1>
            </v-container>
        </div>
        <v-container>
            <v-tabs color="primary accent-4" left>
                <v-tab>Vouchers</v-tab>
                <v-tab>Game Credits</v-tab>
                <v-tab-item v-for="tag in tags" :key="tag">
                    <v-layout row wrap>
                        <RedemptionCard
                            v-for="redemptionDetail in redemptions[tag]"
                            :redemptionDetail="redemptionDetail"
                            :key="redemptionDetail.questionId"
                            @send-points="handlePoints"
                        ></RedemptionCard>
                    </v-layout>
                </v-tab-item>
            </v-tabs>
        </v-container>
    </div>
</template>

<script>
import QuestionCard from "../../components/RedemptionCard";

export default {
    head: {
        title: "Vueducation - Redeem",
    },
    components: {
        QuestionCard,
    },
    middleware: ["auth"],
    data() {
        return {
            points: 1000,
            tags: ["Vouchers", "Game Credits"],
            redemptions: {
                Vouchers: [
                    {
                        questionId: 1,
                        questionTitle: "Grab Ride $10",
                        image: "grab10.png",
                        aos: 1,
                        points: 1000,
                        value: "grab10",
                    },
                    {
                        questionId: 2,
                        questionTitle: "CapitalLand $10",
                        image: "capital10.png",
                        aos: 2,
                        points: 1000,
                        value: "capital10",
                    },
                    {
                        questionId: 3,
                        questionTitle: "Lazada $10",
                        image: "laz10.png",
                        aos: 3,
                        points: 1000,
                        value: "laz10",
                    },
                    {
                        questionId: 7,
                        questionTitle: "Deliveroo $10",
                        image: "deliveroo10.png",
                        aos: 1,
                        points: 1000,
                        value: "deliveroo10",
                    },
                    {
                        questionId: 8,
                        questionTitle: "Shopee $10",
                        image: "shopee10.png",
                        aos: 2,
                        points: 1000,
                        value: "shopee10",
                    },
                    {
                        questionId: 9,
                        questionTitle: "Sephora $10",
                        image: "sephora10.png",
                        aos: 3,
                        points: 1000,
                        value: "sephora10",
                    },
                ],
                "Game Credits": [
                    {
                        questionId: 4,
                        questionTitle: "Cherry Credit $5",
                        points: 500,
                        image: "cherry5000.png",
                        aos: 1,
                        value: "cherry5000",
                    },
                    {
                        questionId: 5,
                        questionTitle: "Steam Credit $10",
                        points: 1000,
                        image: "steam10.png",
                        aos: 2,
                        value: "steam10",
                    },
                    {
                        questionId: 6,
                        questionTitle: "Riot Points $5",
                        points: 500,
                        image: "lol1375.png",
                        aos: 3,
                        value: "lol1375",
                    },
                    {
                        questionId: 10,
                        questionTitle: "Garena Shell $10",
                        points: 1000,
                        image: "garena10.png",
                        aos: 1,
                        value: "garena10",
                    },
                    {
                        questionId: 11,
                        questionTitle: "V-bucks $25",
                        points: 2500,
                        image: "fortnite25.png",
                        aos: 2,
                        value: "fortnite25",
                    },
                    {
                        questionId: 12,
                        questionTitle: "Among Us $100",
                        points: 10000,
                        image: "amongus100.png",
                        aos: 3,
                        value: "amongus100",
                    },
                ],
            },
        };
    },

    mounted() {
        this.$axios.get(`/api/users/${this.$auth.user.username}`).then((res) => {
            this.points = res.data.points;
        });
    },
    methods: {
        handlePoints(points) {
            this.points = points;
        },
    },
};
</script>

<style>
h1 {
    text-align: center;
}

.inline {
    display: inline;
}
</style>
