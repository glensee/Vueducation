<template>
    <div class="body">
        <v-container>
            <v-card class="question">
                <v-flex xs12 sm12 md6 lg8 @click="showImage">
                    <v-img class="image" :src="question.image" />
                </v-flex>

                <v-dialog v-model="imageDialog" max-width="1000px">
                    <v-card>
                        <v-img :src="question.image" />
                    </v-card>
                </v-dialog>

                <v-flex xs12 sm12 md6 lg4 class="detail">
                    <v-flex>
                        <span style="font-size: 2rem">{{ question.questionTitle }}</span>

                        <v-chip v-for="tag of question.questionTag" :key="tag">
                            {{ tag }}
                        </v-chip>

                        <hr />

                        <v-layout align-center>
                            <v-avatar color="primary" size="36">
                                <span class="white--text">
                                    {{ question.initial }}
                                </span>
                            </v-avatar>

                            <span style="margin-left: 10px">
                                {{ question.questioner }}
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

                    <v-flex
                        class="answerButtonContainer"
                        v-if="question.questioner !== this.$auth.user.username"
                    >
                        <v-dialog v-model="dialog" max-width="600px">
                            <template v-slot:activator="{ on, attrs }">
                                <v-btn
                                    class="answerButton"
                                    v-bind="attrs"
                                    v-on="on"
                                    color="primary"
                                >
                                    <span>Answer this Question</span>
                                </v-btn>
                            </template>
                            <v-card>
                                <v-tabs v-model="tab" background-color="transparent" fixed-tabs>
                                    <v-tab>Answer with picture</v-tab>
                                    <v-tab>Answer with text</v-tab>
                                </v-tabs>

                                <v-tabs-items v-model="tab">
                                    <v-tab-item>
                                        <v-card-text>
                                            <v-form
                                                ref="form"
                                                v-model="answerImageValidity"
                                                class="uploadDetail"
                                                @submit.prevent="submit"
                                            >
                                                <v-file-input
                                                    accept="image/png, image/jpeg"
                                                    label="Upload your answer"
                                                    prepend-icon="mdi-camera"
                                                    style="marginbottom: 10px"
                                                    v-model="uploadImage"
                                                    :rules="rules.image"
                                                >
                                                </v-file-input>

                                                <span>Maximum file size: 5mb</span>
                                                <span>Only upload jpg or png image</span>

                                                <v-card-actions>
                                                    <v-btn
                                                        color="primary"
                                                        @click="submitImageAnswer"
                                                        :disabled="!this.answerImageValidity"
                                                    >
                                                        Answer
                                                    </v-btn>
                                                </v-card-actions>
                                            </v-form>
                                        </v-card-text>
                                    </v-tab-item>
                                    <v-tab-item>
                                        <v-card-text>
                                            <v-form
                                                ref="form"
                                                v-model="answerTextValidity"
                                                class="uploadDetail"
                                                @submit.prevent="submit"
                                            >
                                                <v-textarea
                                                    :messages="['Max 500 characters']"
                                                    label="Answer the question here"
                                                    :rules="rules.description"
                                                    v-model="uploadDescription"
                                                    full-width
                                                    filled
                                                    rows="2"
                                                >
                                                </v-textarea>

                                                <v-card-actions>
                                                    <v-btn
                                                        color="primary"
                                                        @click="submitTextAnswer"
                                                        :disabled="!this.answerTextValidity"
                                                    >
                                                        Answer
                                                    </v-btn>
                                                </v-card-actions>
                                            </v-form>
                                        </v-card-text>
                                    </v-tab-item>
                                </v-tabs-items>
                            </v-card>
                        </v-dialog>
                    </v-flex>
                </v-flex>
            </v-card>
        </v-container>

        <v-container v-if="totalAnswer == 1 || totalAnswer == 0">
            <span style="font-size: 2rem">{{ totalAnswer }} answers</span>
        </v-container>

        <v-container v-else>
            <span style="font-size: 2rem">{{ totalAnswer }} answers</span>
        </v-container>

        <AnswerCard
            :answerDetail="bestAnswer"
            :key="bestAnswer.answerId"
            :questioner="question.questioner"
            :bestAnswerId="question.bestAnswerId"
            v-if="bestAnswer !== null"
        ></AnswerCard>

        <AnswerCard
            v-for="answerDetail of answers"
            :answerDetail="answerDetail"
            :key="answerDetail.answerId"
            :questioner="question.questioner"
            :bestAnswerId="question.bestAnswerId"
        ></AnswerCard>
    </div>
</template>

<script>
import AnswerCard from "../../../components/AnswerCard";
import axios from "axios";
export default {
    components: {
        AnswerCard,
    },
    middleware: ["auth"],
    data() {
        return {
            questionId: this.$route.params.question,
            question: [],
            bestAnswer: null,
            answers: [],
            comments: [],
            timeAskInMinutes: null,
            timeAskInHours: null,
            timeAskInDays: null,
            dialog: false,
            imageDialog: false,
            answerImageValidity: true,
            answerTextValidity: true,
            totalAnswer: 0,
            rules: {
                description: [(val) => (val || "").length > 0 || "Please include description"],
                image: [
                    (v) => !!v || "Image is required",
                    (v) => !v || v.size < 5242880 || "Max 5 MB",
                    (v) =>
                        !v ||
                        v.type === "image/png" ||
                        v.type === "image/jpeg" ||
                        "Only jpg and png are allowed",
                ],
            },
            uploadDescription: "",
            uploadImage: undefined,
            tab: null,
        };
    },
    head() {
        return {
            title: `Vueducation - ${this.question.questionTitle}`,
        };
    },

    async fetch() {
        let questionResponse = await this.$axios.get("/api/getQuestionById/" + this.questionId);
        this.question = questionResponse.data[0];

        let answerResponse = await this.$axios.get("/api/getAnswerByQuestionId/" + this.questionId);

        if (this.question.bestAnswerId !== null) {
            this.bestAnswer = answerResponse.data.filter(
                (answer) => parseInt(answer.answerId) === parseInt(this.question.bestAnswerId)
            )[0];
            this.answers = answerResponse.data.filter(
                (answer) => parseInt(answer.answerId) !== parseInt(this.question.bestAnswerId)
            );
            this.totalAnswer = this.answers.length + 1;
        } else {
            this.answers = answerResponse.data;
            this.totalAnswer = this.answers.length;
        }

        let dateNow = new Date();
        let timestamp = Math.round(
            (dateNow.getTime() / 1000 - Math.round(this.question.timeAsked)) / 60
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
    methods: {
        showImage() {
            this.imageDialog = true;
        },
        close() {
            this.dialog = false;
            this.$refs.form.reset();
        },
        async submitImageAnswer() {
            let formData = new FormData();

            const toBase64 = (file) =>
                new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = () => resolve(reader.result.split(",")[1]);
                    reader.onerror = (error) => reject(error);
                });

            var imageBase64 = await toBase64(this.uploadImage);

            formData.append("questionId", this.question.questionId);
            formData.append("answeredBy", this.$auth.user.username);
            formData.append("filename", this.uploadImage.name);
            formData.append("image", imageBase64);
            formData.append("description", null);

            await axios
                .post(process.env.NUXT_ENV_BACKEND + "/postAnswer", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                })
                .catch((err) => {
                    console.log(err.data);
                });
            this.dialog = false;
            window.location.reload();
        },
        async submitTextAnswer() {
            let formData = new FormData();
            formData.append("questionId", this.question.questionId);
            formData.append("answeredBy", this.$auth.user.username);
            formData.append("image", null);
            formData.append("filename", null);
            formData.append("description", this.uploadDescription);

            await axios
                .post(process.env.NUXT_ENV_BACKEND + "/postAnswer", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                })
                .catch((err) => {
                    console.log(err.data);
                });
            console.log("text");

            this.dialog = false;
            window.location.reload(true);
        },
    },
    middleware: ["auth"],
};
</script>

<style lang="scss">
.answerButton {
    margin-top: 10px;
    vertical-align: bottom;
}

.question {
    border-radius: 1rem;
    padding: 2rem;
    margin-top: 10px;
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

.v-chip {
    margin-right: 10px;
}

.answerButtonContainer {
    display: flex;
    align-items: flex-end;
}

hr {
    margin: 10px 0px;
}

.v-tab-item {
    width: 100%;
}

.uploadDetail {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.v-file-input {
    width: 100%;
}

.v-textarea {
    width: 100%;
}

@media (max-width: 959px) {
    .detail {
        display: flex;
        flex-direction: column;
        padding: 0;
        margin-top: 10px;
    }

    .question {
        border-radius: 1rem;
        padding: 2rem;
        margin: 10px auto;
        display: block;
    }

    .v-slide-group__prev,
    .v-slide-group__prev--disabled {
        display: none !important;
    }
}
</style>
