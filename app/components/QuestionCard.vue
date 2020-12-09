<template>
    <v-flex xs12 md6 lg4>
        <v-card
            :loading="loading"
            data-aos="fade-up-right"
            data-aos-delay="500"
            v-if="this.index % 3 === 0"
        >
            <nuxt-link :to="`app/question/${questionDetail.questionId}`">
                <v-img class="pointer" :src="questionDetail.image" height="200px" />
            </nuxt-link>
            <v-card-text>
                <v-chip v-for="tag of questionDetail.questionTag" :key="tag">
                    {{ tag }}
                </v-chip>
            </v-card-text>

            <v-layout align-baseline>
                <v-flex lg6 md6 xs6>
                    <v-card-title
                        class="pointer questionTitle"
                        @click="$router.push(`app/question/${questionDetail.questionId}`)"
                    >
                        <div class="questionTitle">
                            {{ questionDetail.questionTitle }}
                        </div>
                    </v-card-title>

                    <v-card-text>
                        <span style="font-size: 200%">{{ this.numberOfAnswer }}</span>
                        <span>answers</span>
                    </v-card-text>
                </v-flex>
                <v-flex :style="{ justifyContent: `right` }">
                    <v-layout align-center>
                        <v-avatar color="primary" size="36">
                            <span class="white--text">
                                {{ questionDetail.initial }}
                            </span>
                        </v-avatar>
                        <span style="margin-left: 10px">
                            {{ questionDetail.questioner }}
                        </span>
                    </v-layout>
                    <span v-if="this.timeAskInMinutes !== null">
                        asked {{ this.timeAskInMinutes }} mins ago
                    </span>

                    <span v-else-if="this.timeAskInHours !== null">
                        asked {{ this.timeAskInHours }} hours ago
                    </span>

                    <span v-else> asked {{ this.timeAskInDays }} days ago </span>
                </v-flex>
            </v-layout>
        </v-card>

        <v-card
            :loading="loading"
            data-aos="fade-up"
            data-aos-delay="1000"
            v-else-if="this.index % 3 === 1"
        >
            <v-img
                class="pointer questionTitle"
                :src="questionDetail.image"
                height="200px"
                @click="$router.push(`app/question/${questionDetail.questionId}`)"
            />

            <v-card-text>
                <v-chip v-for="tag of questionDetail.questionTag" :key="tag">
                    {{ tag }}
                </v-chip>
            </v-card-text>

            <v-layout align-baseline>
                <v-flex lg6 md6 xs6>
                    <v-card-title
                        class="pointer"
                        @click="$router.push(`app/question/${questionDetail.questionId}`)"
                    >
                        <div class="questionTitle">
                            {{ questionDetail.questionTitle }}
                        </div></v-card-title
                    >
                    <v-card-text>
                        <span style="font-size: 200%">{{ numberOfAnswer }}</span>
                        <span>answers</span>
                    </v-card-text>
                </v-flex>
                <v-flex :style="{ justifyContent: `right` }">
                    <v-layout align-center>
                        <v-avatar color="primary" size="36">
                            <span class="white--text">
                                {{ questionDetail.initial }}
                            </span>
                        </v-avatar>
                        <span style="margin-left: 10px">
                            {{ questionDetail.questioner }}
                        </span>
                    </v-layout>
                    <span v-if="this.timeAskInMinutes !== null">
                        asked {{ this.timeAskInMinutes }} mins ago
                    </span>

                    <span v-else-if="this.timeAskInHours !== null">
                        asked {{ this.timeAskInHours }} hours ago
                    </span>

                    <span v-else> asked {{ this.timeAskInDays }} days ago </span>
                </v-flex>
            </v-layout>
        </v-card>

        <v-card
            :loading="loading"
            data-aos="fade-up-left"
            data-aos-delay="1500"
            v-else-if="this.index % 3 === 2"
        >
            <v-img
                class="pointer"
                :src="questionDetail.image"
                height="200px"
                @click="$router.push(`app/question/${questionDetail.questionId}`)"
            />

            <v-card-text>
                <v-chip v-for="tag of questionDetail.questionTag" :key="tag">
                    {{ tag }}
                </v-chip>
            </v-card-text>

            <v-layout align-baseline>
                <v-flex lg6 md6 xs6>
                    <v-card-title
                        class="pointer questionTitle"
                        @click="$router.push(`app/question/${questionDetail.questionId}`)"
                    >
                        <div class="questionTitle">
                            {{ questionDetail.questionTitle }}
                        </div></v-card-title
                    >
                    <v-card-text>
                        <span style="font-size: 200%">{{ this.numberOfAnswer }}</span>
                        <span>answers</span>
                    </v-card-text>
                </v-flex>
                <v-flex :style="{ justifyContent: `right` }">
                    <v-layout align-center>
                        <v-avatar color="primary" size="36">
                            <span class="white--text">
                                {{ questionDetail.initial }}
                            </span>
                        </v-avatar>
                        <span style="margin-left: 10px">
                            {{ questionDetail.questioner }}
                        </span>
                    </v-layout>
                    <span v-if="this.timeAskInMinutes !== null">
                        asked {{ this.timeAskInMinutes }} mins ago
                    </span>

                    <span v-else-if="this.timeAskInHours !== null">
                        asked {{ this.timeAskInHours }} hours ago
                    </span>

                    <span v-else> asked {{ this.timeAskInDays }} days ago </span>
                </v-flex>
            </v-layout>
        </v-card>
    </v-flex>
</template>

<script>
export default {
    name: "QuestionCard",
    props: ["questionDetail", "index"],

    data() {
        return {
            loading: true,
            numberOfAnswer: 0,
            timeAskInMinutes: null,
            timeAskInHours: null,
            timeAskInDays: null,
        };
    },

    async fetch() {
        let response = await this.$axios.get(
            "/api/getAnswerByQuestionId/" + this.questionDetail.questionId
        );

        this.numberOfAnswer = response.data.length;
    },

    methods: {
        getImage(image) {
            return require("../assets/question/" + image);
        },
    },

    mounted() {
        this.loading = false;

        let dateNow = new Date();
        let timestamp = Math.round(
            (dateNow.getTime() / 1000 - Math.round(this.questionDetail.timeAsked)) / 60
        );
        if (timestamp < 60) {
            this.timeAskInMinutes = timestamp;
        } else {
            let timeInHour = parseInt(timestamp / 60);
            if (timeInHour < 24) {
                this.timeAskInHours = timeInHour;
            } else {
                this.timeAskInDays = parseInt(timeInHour / 24);
            }
        }
    },
};
</script>

<style lang="scss" scoped>
.v-card {
    margin: 8px;
}
.pointer {
    cursor: pointer;
}
.v-chip {
    margin-right: 5px;
}
.questionTitle {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
