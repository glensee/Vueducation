<template>
    <v-container>
        <v-card class="answer" :class="{ bestAnswer: bestAnswerId == answerDetail.answerId }">
            <v-flex xs12 md6 lg8 v-if="this.answerDetail.image !== null" @click="showImage">
                <v-img class="image" :src="answerDetail.image" />
            </v-flex>

            <v-flex xs12 md6 lg8 class="center" v-else-if="this.answerDetail.image === null">
                {{ this.answerDetail.description }}
            </v-flex>

            <v-dialog
                v-model="imageDialog"
                max-width="1000px"
                v-if="this.answerDetail.image !== null"
                scrollable
            >
                <v-card>
                    <v-img :src="answerDetail.image" />
                </v-card>
            </v-dialog>

            <v-flex xs12 md6 lg4 class="detail">
                <v-flex>
                    <v-layout>
                        <v-flex class="iconContainer">
                            <v-icon
                                :class="{ active: iconActive === 'check' }"
                                class="voteIcon"
                                color="green"
                                x-large
                                @click="activeCheck"
                            >
                                mdi-thumb-up
                            </v-icon>
                        </v-flex>
                        <span class="vote" v-if="vote == 1 || vote == 0 || vote == -1"
                            ><strong>{{ vote }} vote</strong></span
                        >
                        <span class="vote" v-else
                            ><strong>{{ vote }} votes</strong></span
                        >

                        <v-img
                            :src="require('~/assets/star.png')"
                            max-width="45px"
                            v-if="bestAnswerId == answerDetail.answerId"
                        ></v-img>
                    </v-layout>

                    <hr />

                    <v-layout align-center>
                        <v-avatar color="primary" size="36">
                            <span class="white--text">
                                {{ answerDetail.initial }}
                            </span>
                        </v-avatar>
                        <span style="margin-left: 10px">
                            {{ answerDetail.answeredBy }}
                        </span>
                    </v-layout>

                    <span v-if="this.timeAnswerInMinutes !== null">
                        answered {{ this.timeAnswerInMinutes }} mins ago
                    </span>

                    <span v-else-if="this.timeAnswerInHours !== null">
                        answered {{ this.timeAnswerInHours }} hours ago
                    </span>

                    <span v-else> answered {{ this.timeAnswerInDays }} days ago </span>
                </v-flex>
                <v-flex
                    class="buttonContainer"
                    v-if="
                        bestAnswerId == answerDetail.answerId &&
                        questioner === this.$auth.user.username
                    "
                >
                    <v-btn class="sendMessageButton" color="primary" @click="initiateConversation">
                        <span>Send Message</span>
                    </v-btn>
                </v-flex>
                <v-flex
                    class="buttonContainer"
                    v-if="bestAnswerId === null && questioner === this.$auth.user.username"
                >
                    <v-btn class="bestAnswerButton" @click="markBestAnswer" color="primary">
                        <span>Mark as best answer</span>
                    </v-btn>
                </v-flex>
            </v-flex>
        </v-card>
    </v-container>
</template>

<script>
export default {
    name: "AnswerCard",
    props: ["answerDetail", "questioner", "bestAnswerId"],
    data() {
        return {
            comments: [],
            iconActive: "none",
            userVote: 0,
            vote: 0,
            timeAnswerInMinutes: null,
            timeAnswerInHours: null,
            timeAnswerInDays: null,
            imageDialog: false,
        };
    },
    async fetch() {
        let commentResponse = await this.$axios.get(
            "/api/getCommentByAnswerId/" + this.answerDetail.answerId
        );
        this.comments = commentResponse.data;

        let voteResponse = await this.$axios.get(
            "/api/getVoteByAnswerId/" + this.answerDetail.answerId
        );
        this.vote = voteResponse.data.vote;

        let userVoteResponse = await this.$axios.get(
            "/api/getVoteByAnswerIdUser/" +
                this.answerDetail.answerId +
                "/" +
                this.$auth.user.username
        );
        this.userVote = userVoteResponse.data.vote;

        if (this.userVote == 1) {
            this.iconActive = "check";
        } else if (this.userVote == -1) {
            this.iconActive = "none";
        }
    },
    methods: {
        showImage() {
            this.imageDialog = true;
        },
        async markBestAnswer() {
            let response = await this.$axios.get(
                `/api/markBestAnswer/${this.answerDetail.questionId}/${this.answerDetail.answerId}`
            );
            let pointResponse = await this.$axios.put(
                `/api/users/${this.answerDetail.answeredBy}/points/add/20`
            );
            window.location.reload();
        },
        async activeCheck() {
            let voteResponse = await this.$axios.get(
                `/api/postVote/${this.answerDetail.answerId}/${this.$auth.user.username}/1`
            );
            this.vote = voteResponse.data.vote;
            if (this.iconActive === "check") {
                this.iconActive = "none";
            } else {
                this.iconActive = "check";
            }
        },
        async initiateConversation() {
            let currentUser = this.$auth.user.username;

            const ref = this.$fire.firestore.collection("conversation").doc(currentUser);
            const ref2 = this.$fire.firestore
                .collection("conversation")
                .doc(this.answerDetail.answeredBy);
            let snap;
            let snap2;
            try {
                snap = await ref.get();
                let friends = snap.data().friends;
                if (!friends.includes(this.answerDetail.answeredBy)) {
                    friends.push(this.answerDetail.answeredBy);
                }

                const result = await ref.update({ friends: friends });

                snap2 = await ref2.get();
                let friends2 = snap2.data().friends;
                if (!friends2.includes(this.questioner)) {
                    friends2.push(this.questioner);
                }

                const result2 = await ref2.update({ friends: friends2 });
            } catch (e) {
                console.error(e);
            }
            this.$router.push("/app/chat");
        },
    },
    mounted() {
        let dateNow = new Date();
        let timestamp = Math.round(
            (dateNow.getTime() / 1000 - Math.round(this.answerDetail.timeAnswered)) / 60
        );

        if (timestamp < 60) {
            this.timeAnswerInMinutes = timestamp;
        } else {
            let timeInHour = parseInt(timestamp / 60);
            if (timeInHour < 24) {
                this.timeAnswerInHours = timeInHour;
            } else {
                this.timeAnswerInDays = parseInt(timeInHour / 24);
            }
        }
    },
};
</script>

<style lang="scss" scoped>
.bestAnswer {
    border: 5px solid lightgreen;
}

.voteIcon {
    margin-right: 10px;
    filter: grayscale(100%);
    cursor: pointer;
}

.vote {
    display: flex;
    flex: 1 1 auto;
    align-items: center;
}

.active {
    filter: none;
}

.answer {
    border-radius: 1rem;
    padding: 2rem;
    margin: 10px auto;
    display: flex;
}

.image {
    max-height: 500px;
    height: 100%;
}

.detail {
    display: flex;
    flex-direction: column;
    padding: 0 2rem;
}

hr {
    margin: 10px 0px;
}

.center {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2rem;
}

.buttonContainer {
    margin-top: 10px;
    display: flex;
    align-items: flex-end;
}

.sendMessageButton {
    vertical-align: bottom;
}

.bestAnswerButton {
    vertical-align: bottom;
}

.iconContainer {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    flex: 0 1 auto !important;
}

@media (max-width: 959px) {
    .detail {
        display: flex;
        flex-direction: column;
        padding: 0;
        margin-top: 10px;
    }

    .answer {
        border-radius: 1rem;
        padding: 2rem;
        margin: 10px auto;
        display: block;
    }
}
</style>
