<template>
    <v-flex xs12 md6 lg4 xl3>
        <v-dialog v-model="dialog" persistent max-width="400">
            <template v-slot:activator="{ on, attrs }">
                <v-card
                    :loading="loading"
                    data-aos="fade-up-right"
                    data-aos-delay="500"
                    v-if="redemptionDetail.aos === 1"
                    max-width="400"
                    max-height="400"
                >
                    <v-img :src="getImage(redemptionDetail.image)" max-height="300" />
                    <v-row>
                        <v-col cols="7">
                            <v-card-title>{{ redemptionDetail.questionTitle }}</v-card-title>
                            <v-card-subtitle class="font-weight-bold">
                                {{ redemptionDetail.points }} points
                            </v-card-subtitle>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col cols="5">
                            <v-btn color="primary" class="mt-6" v-bind="attrs" v-on="on">
                                Redeem
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card>

                <v-card
                    :loading="loading"
                    data-aos="fade-up"
                    data-aos-delay="1000"
                    v-else-if="redemptionDetail.aos === 2"
                    max-width="400"
                    max-height="400"
                >
                    <v-img :src="getImage(redemptionDetail.image)" max-height="300" />
                    <v-row>
                        <v-col cols="7">
                            <v-card-title>{{ redemptionDetail.questionTitle }}</v-card-title>
                            <v-card-subtitle class="font-weight-bold">
                                {{ redemptionDetail.points }} points
                            </v-card-subtitle>
                        </v-col>
                        <v-col cols="5">
                            <v-btn color="primary" class="mt-6" v-bind="attrs" v-on="on">
                                Redeem
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card>

                <v-card
                    :loading="loading"
                    data-aos="fade-up-left"
                    data-aos-delay="1500"
                    v-else-if="redemptionDetail.aos === 3"
                    max-width="400"
                    max-height="400"
                >
                    <v-img :src="getImage(redemptionDetail.image)" max-height="300" />
                    <v-row>
                        <v-col cols="7">
                            <v-card-title>{{ redemptionDetail.questionTitle }}</v-card-title>
                            <v-card-subtitle class="font-weight-bold">
                                {{ redemptionDetail.points }} points
                            </v-card-subtitle>
                        </v-col>
                        <v-col cols="5">
                            <v-btn color="primary" class="mt-6" v-bind="attrs" v-on="on">
                                Redeem
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card>
            </template>
            <div class="text-left">
                <v-card v-if="redeemed">
                    <v-card-title class="headline success--text font-weight-bold">
                        Success!
                    </v-card-title>
                    <v-card-text>
                        Your code is:
                        <div class="grey lighten-3 rounded d-inline-block">
                            {{ code }}
                        </div>
                        <br />
                        You have {{ points }} remaining points.
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="primary darken-1"
                            text
                            @click="
                                dialog = false;
                                redeemed = false;
                            "
                        >
                            Exit
                        </v-btn>
                    </v-card-actions>
                </v-card>
                <v-card v-else-if="error">
                    <v-card-title class="headline error--text font-weight-bold">
                        Failure
                    </v-card-title>
                    <v-card-text>{{ error }}</v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="primary darken-1"
                            text
                            @click="
                                dialog = false;
                                error = '';
                            "
                        >
                            Exit
                        </v-btn>
                    </v-card-actions>
                </v-card>
                <v-card v-else>
                    <v-card-title class="headline"> Are you sure? </v-card-title>
                    <v-card-text
                        >You are redeeming {{ redemptionDetail.questionTitle }} of
                        {{ redemptionDetail.points }} points.</v-card-text
                    >
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary darken-1" text @click="dialog = false"> No </v-btn>
                        <v-btn color="primary darken-2" text @click="confirm(redemptionDetail)">
                            Yes
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </div>
        </v-dialog>
    </v-flex>
</template>

<script>
export default {
    name: "QuestionCard",
    props: ["redemptionDetail"],

    data() {
        return {
            dialog: false,
            loading: true,
            redeemed: false,
            points: 0,
            error: false,
            code: null,
        };
    },

    methods: {
        getImage(image) {
            return require("../assets/redemption/" + image);
        },
        confirm: async function (redemptionDetail) {
            let points = await this.$axios.get(`/api/users/${this.$auth.user.username}`);

            points = points.data.points;

            if (points < redemptionDetail.points) {
                this.error = "You have insufficient points.";
            } else {
                try {
                    let deduct = await this.$axios.put(
                        `/api/users/${this.$auth.user.username}/points/deduct/${redemptionDetail.points}`
                    );

                    let code = await this.$axios.get(`/api/promo/${redemptionDetail.value}`);

                    this.redeemed = true;
                    this.points = points - redemptionDetail.points;
                    this.$emit("send-points", this.points);
                    this.code = code.data.code;
                } catch (e) {
                    this.error = "An error occurred during redemption";
                }
            }
        },
    },

    mounted() {
        this.loading = false;
        this.$axios.get(`/api/users/${this.$auth.user.username}`).then((res) => {
            this.points = res.data.points;
        });
    },
};
</script>

<style lang="scss" scoped>
.v-card {
    margin: 8px;
}
</style>
