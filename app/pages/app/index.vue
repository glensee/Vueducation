<template>
    <div class="body">
        <div class="heading">
            <v-container>
                <h1>PROBLEM WITH HOMEWORK?</h1>
                <h1>ASK A QUESTION HERE</h1>

                <v-dialog v-model="dialog" max-width="600px">
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            class="askQuestionButton"
                            v-bind="attrs"
                            v-on="on"
                        >
                            <span class="askQuestionText">Ask a question</span>
                        </v-btn>
                    </template>
                    <v-card>
                        <v-form
                            ref="form"
                            v-model="formValidity"
                            class="uploadQuestionCard"
                            @submit.prevent="submit"
                        >
                            <v-card-actions style="alignSelf: flex-end">
                                <v-icon @click="close"> mdi-close </v-icon>
                            </v-card-actions>

                            <v-card-title style="marginbottom: 10px">
                                <span class="headline">Have a question?</span>
                            </v-card-title>

                            <v-card-text>
                                <span style="marginbottom: 10px"
                                    >Snap a photo of ONE homework problem and
                                    upload below.</span
                                >
                                <v-layout>
                                    <v-select
                                        :items="
                                            subjects.filter(
                                                (subject) => subject !== `All`
                                            )
                                        "
                                        label="Choose Subject"
                                        outlined
                                        class="pa-2 uploadFilter"
                                        v-model="uploadSubject"
                                        :rules="rules.subject"
                                    />
                                    <v-select
                                        :items="
                                            levels.filter(
                                                (level) => level !== `All`
                                            )
                                        "
                                        label="Choose Level"
                                        outlined
                                        class="pa-2 uploadFilter"
                                        v-model="uploadLevel"
                                        :rules="rules.level"
                                    />
                                </v-layout>

                                <v-text-field
                                    :messages="['Max 20 characters']"
                                    label="Question Title"
                                    :rules="rules.description"
                                    v-model="uploadDescription"
                                    placeholder="e.g. How to score A+ on WAD II?"
                                    required
                                >
                                </v-text-field>

                                <v-file-input
                                    accept="image/png, image/jpeg"
                                    label="Upload your question"
                                    prepend-icon="mdi-camera"
                                    style="marginbottom: 10px"
                                    v-model="uploadImage"
                                    :rules="rules.image"
                                >
                                </v-file-input>
                                <span>Maximum file size: 5mb</span>
                                <span>Only upload jpg or png image</span>
                            </v-card-text>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    color="primary"
                                    @click="submitForm"
                                    :disabled="!this.formValidity"
                                >
                                    Ask
                                </v-btn>
                            </v-card-actions>
                        </v-form>
                    </v-card>
                </v-dialog>
            </v-container>
        </div>
        <v-container class="filter">
            <v-layout row wrap>
                <v-flex xs12 md6 lg3>
                    <v-select
                        :items="subjects"
                        label="Choose Subject"
                        outlined
                        class="pa-2"
                        v-model="subjectFilter"
                        @change="handleFilter()"
                    />
                </v-flex>
                <v-flex xs12 md6 lg3>
                    <v-select
                        :items="levels"
                        label="Choose Level"
                        outlined
                        class="pa-2"
                        v-model="levelFilter"
                        @change="handleFilter()"
                    />
                </v-flex>
            </v-layout>
            <v-layout row wrap>
                <v-flex>
                    <v-chip-group
                        v-model="answerFilter"
                        active-class="blue accent-4 white--text"
                        column
                        @change="handleFilter()"
                    >
                        <v-chip value="All">ALL</v-chip>

                        <v-chip value="Answered">ANSWERED</v-chip>

                        <v-chip value="Unanswered">UNANSWERED</v-chip>
                    </v-chip-group>
                </v-flex>
            </v-layout>
        </v-container>

        <v-container>
            <v-layout row wrap>
                <QuestionCard
                    v-for="(questionDetail, index) in filteredQuestion"
                    :questionDetail="questionDetail"
                    :index="index"
                    :key="questionDetail.questionId"
                ></QuestionCard>
            </v-layout>
        </v-container>
    </div>
</template>
    </div>
</template>

<script>
import axios from "axios";
import QuestionCard from "../../components/QuestionCard";
export default {
    head: {
        title: "Vueducation - Home"
    },
    middleware: ["auth"],
    components: {
        QuestionCard,
    },
    data() {
        return {
            subjectFilter: "All",
            levelFilter: "All",
            answerFilter: "Unanswered",
            subjects: [
                "All",
                "Biology",
                "Chemistry",
                "Mathematics",
                "Physics",
                "Programming",
            ],
            levels: ["All", "Primary", "Secondary", "JC", "Bachelor"],
            questions: [],
            filteredQuestion: [],
            dialog: false,
            formValidity: true,
            rules: {
                description: [
                    (val) =>
                        (val || "").length > 0 || "Please include description",
                    (val) =>
                        (val || "").length < 20 ||
                        "Please use less than 20 characters",
                ],
                image: [
                    (v) => !!v || "Image is required",
                    (v) => !v || v.size < 5242880 || "Max 5 MB",
                    (v) =>
                        !v ||
                        v.type === "image/png" ||
                        v.type === "image/jpeg" ||
                        "Only jpg and png are allowed",
                ],
                subject: [(val) => !!val || "Subject is required"],
                level: [(val) => !!val || "Level is required"],
            },
            uploadSubject: "",
            uploadLevel: "",
            uploadDescription: "",
            uploadImage: undefined
        };
    },

    async fetch() {
        let questionResponse = await this.$axios.get("/api/getQuestions");

        let responseData = questionResponse.data;

        for (let question of responseData) {
            let answerResponse = await this.$axios.get(
                "/api/getAnswerByQuestionId/" + question.questionId
            );
            question.numberOfAnswer = answerResponse.data.length;
        }
        this.questions = questionResponse.data;
        this.filteredQuestion = questionResponse.data.filter(question => question.bestAnswerId === null);
    },

    methods: {
        handleFilter() {
            var result = this.questions;

            if (this.subjectFilter !== "All") {
                result = result.filter((question) => {
                    const res = question.questionTag.filter(
                        (tag) => this.subjectFilter === tag
                    );
                    return res.length > 0;
                });
            }
            if (this.levelFilter !== "All") {
                result = result.filter((question) => {
                    const res = question.questionTag.filter(
                        (tag) => this.levelFilter === tag
                    );
                    return res.length > 0;
                });
            }

            if (this.answerFilter !== "All") {
                this.filteredQuestion = result.filter((question) => {
                    var answered = question.bestAnswerId !== null;
                    return this.answerFilter === "Answered"
                        ? answered
                        : !answered;
                });
            } else {
                this.filteredQuestion = result;
            }
        },
        close() {
            this.dialog = false;
            this.$refs.form.reset();
        },
        async submitForm() {
            let formData = new FormData();

            let questionTag = [this.uploadSubject, this.uploadLevel];

            const toBase64 = file => new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => resolve(reader.result.split(",")[1]);
                reader.onerror = error => reject(error);
            });

            var imageBase64 = await toBase64(this.uploadImage);

            formData.append("questionTag", questionTag);
            formData.append("questionTitle", this.uploadDescription);
            formData.append("questioner", this.$auth.user.username);
            formData.append("filename", this.uploadImage.name);
            formData.append("image", imageBase64);

            await axios
                .post(process.env.NUXT_ENV_BACKEND + "/addQuestion", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                })
                .catch((err) => {
                    console.log(err.data);
                });

            this.dialog = false;
            window.location.reload()
        },
    },
};
</script>

<style>
body {
    overflow: hidden;
}

h1 {
    color: white;
}

.heading {
    text-align: center;
    background-image: url("../../assets/background.jpg");
    background-size: cover;
}

.inline {
    display: inline;
}

.askQuestionText {
    font-size: 150%;
    padding: 10px;
    color: white;
}

.filter .v-chip {
    width: 150px;
    justify-content: center;
}

.v-chip-group {
    margin: 0px 10px;
}

.askQuestionButton {
    background: transparent !important;
    border: 1px solid white !important;
    border-radius: 30px !important;
    margin-top: 20px !important;
}

.uploadQuestionCard {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.uploadFilter {
    width: 100%;
}
</style>
