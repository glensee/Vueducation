<template>
    <div style="width: 90%; margin: auto; margin-bottom: 32px">
        <span class="text-md-h5 py-4 font-weight-medium">Create new workshop</span>

        <v-form ref="newworkshopform" v-model="formValidity" @submit.prevent="submit">
            <v-text-field
                label="Workshop Name"
                outlined
                :rules="rules.name"
                v-model="workshopName"
                clearable
            ></v-text-field>
            <v-text-field
                label="Institute"
                :rules="rules.name"
                outlined
                v-model="institute"
                clearable
            ></v-text-field>
            <v-row>
                <v-col cols="6">
                    <v-combobox
                        :items="categories"
                        label="Category"
                        outlined
                        v-model="category"
                        clearable
                        required
                        :rules="rules.category"
                    ></v-combobox>
                </v-col>
                <v-col cols="6">
                    <v-file-input
                        :rules="rules.file"
                        label="Photo"
                        outlined
                        prepend-icon="mdi-camera"
                        v-model="image"
                        required
                        show-size
                        accept="image/png, image/jpeg"
                    ></v-file-input>

                    <!-- <dropzone
            ref="myVueDropzone"
            id="dropzone"
            :options="dropzoneOptions"
          ></dropzone> -->
                </v-col>
            </v-row>

            <v-row>
                <v-col lg="6" md="12">
                    <v-row>
                        <v-col>
                            <p>Start Date</p>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col style="text-align: center">
                            <v-date-picker
                                v-model="startDate"
                                :reactive="true"
                                :landscape="$vuetify.breakpoint.mdAndUp"
                            ></v-date-picker>
                        </v-col>
                        <v-col style="text-align: center">
                            <v-time-picker
                                format="24hr"
                                :landscape="$vuetify.breakpoint.mdAndUp"
                                v-model="startTime"
                                ampm-in-title
                            ></v-time-picker>
                        </v-col>
                    </v-row>
                </v-col>

                <v-col lg="6" md="12">
                    <v-row>
                        <v-col>
                            <p>End Date</p>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col style="text-align: center">
                            <v-date-picker
                                v-model="endDate"
                                :reactive="true"
                                :landscape="$vuetify.breakpoint.mdAndUp"
                            ></v-date-picker>
                        </v-col>
                        <v-col style="text-align: center">
                            <v-time-picker
                                format="24hr"
                                :landscape="$vuetify.breakpoint.mdAndUp"
                                v-model="endTime"
                                ampm-in-title
                            ></v-time-picker>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>

            <v-textarea
                class="mt-5"
                :rules="rules.description"
                label="Description"
                outlined
                required
                v-model="description"
                clearable
            ></v-textarea>

            <v-radio-group v-model="mode" row>
                <v-radio label="Online" value="online" checked></v-radio>
                <v-radio label="Physical" value="physical"></v-radio>
            </v-radio-group>

            <div v-if="mode == 'online'">
                <v-text-field
                    :rules="rules.link"
                    label="Livestream Link"
                    outlined
                    v-model="link"
                    clearable
                    :required="mode == `online`"
                    v-if="mode == 'online'"
                ></v-text-field>
            </div>

            <div v-if="mode == 'physical'">
                <googlePlaces
                    :getLatLng="{ lat: lat, lng: lng }"
                    :parentMode="mode"
                    v-on:getLatLng="getLatLng"
                    v-if="mode == 'physical'"
                />
            </div>
        </v-form>

        <v-row>
            <v-btn color="normal" @click="resetForm()" style="margin-right: 20px">reset</v-btn>

            <v-btn
                color="primary"
                @click="submitForm()"
                :disabled="
                    !this.formValidity ||
                    (this.mode == 'physical' && this.lat == 0 && this.lng == 0)
                "
                >Submit</v-btn
            >

        </v-row>

        <v-snackbar v-model="snackbar">
            {{ snackbarMessage }}
            <v-btn
                text
                color="primary"
                @click.native="snackbar = false"
                :to="this.snackbarMessage == 'success' ? '/app/workshop/main' : ''"
                >Close</v-btn
            >
        </v-snackbar>
    </div>
</template>

<script>
import axios from "axios";
import googlePlaces from "./googlePlaces";
import Dropzone from "nuxt-dropzone";
import "vue2-dropzone/dist/vue2Dropzone.min.css";

export default {
    head: {
        title: `Vueducation - Create Workshop`,
    },
    middleware: ["auth"],

    components: {
        axios,
        googlePlaces,
        Dropzone,
    },

    data() {
        return {
            formValidity: true,
            snackbar: false,
            snackbarMessage: "",
            snackbarLink: "",
            workshopName: "",
            institute: "",
            category: "",
            startDate: new Date().toISOString().substr(0, 10),
            endDate: new Date().toISOString().substr(0, 10),
            startTime: `14:00`,
            endTime: `15:00`,
            image: undefined,
            link: "",
            lat: 0,
            lng: 0,
            description: "",
            mode: "online",
            categories: ["Physics"],
            livestreamLinkStyle: "display: block;",
            rules: {
                name: [(val) => (val || "").length > 0 || "This field is required"],
                description: [
                    (val) =>
                        (val || "").split(" ").length > 50 ||
                        "Please use more than 50 words to describe your workshop",
                ],
                link: [
                    (val) =>
                        ((val || "").substring(0, 4) == "http" && (val || "").length > 4) ||
                        "Please provide a valid URL.",
                    (val) =>
                        (val || "").substring(0, "https://www.youtube.com".length) ==
                            "https://www.youtube.com" ||
                        "Apologies, we only accept youtube links for now.",
                ],
                file: [
                    (value) =>
                        !value || value.size < 2000000 || "Avatar size should be less than 2 MB!",
                ],
                category: [(value) => value != "" || "Please select or enter a category"],
            },
            dropzoneOptions: {
                url: "https://httpbin.org/post",
                thumbnailWidth: 150,
                maxFilesize: 0.5,
                headers: { "My-Awesome-Header": "header value" },
            },
        };
    },
    computed: {
        isFormValid() {
            return;
        },
    },

    methods: {
        getMode() {
            return this.mode;
        },
        resetForm() {
            this.$refs.newworkshopform.reset();
        },
        convertTime(time) {
            if (time.split(":")[1] < 10) {
                return time.split(":")[0] + ":0" + time.split(":")[1];
            }
            return time;
        },
        testDate() {
            // Start and end datetime for internal calendar
            let localeStartDate = new Date(
                Date.parse(this.startDate + "T" + this.convertTime(this.startTime))
            );
            // localeStartDate = new Date(localeStartDate.setTime(localeStartDate.getTime() + (8 * 60 * 60 * 1000))).toUTCString();
            console.log(localeStartDate);
            localeStartDate.setHours(localeStartDate.getHours() -8 )

            let localeEndDate = new Date(
                Date.parse(this.endDate + "T" + this.convertTime(this.endTime))
            );
            localeEndDate = new Date(localeEndDate.setHours(localeEndDate.getHours() + 8)).toString();
            console.log(localeStartDate);
        },
        submitForm() {
            let formData = new FormData();
            let location = "";
            if (this.lat != "" && this.lng != "") {
                location = this.lat + "," + this.lng;
            }

            console.log(this.startDate);

            formData.append("image", this.image);
            formData.append("name", this.workshopName);
            formData.append("institution", this.institute);
            formData.append("description", this.description);
            formData.append("category", this.category);
            formData.append("link", this.link);
            formData.append("location", location);
            formData.append("mode", this.mode);
            formData.append("startDate", this.startDate);
            formData.append("startTime", this.startTime);
            formData.append("endDate", this.endDate);
            formData.append("endTime", this.endTime);

            // Start and end datetime for internal calendar
            let localeStartDate = new Date(
                Date.parse(this.startDate + "T" + this.convertTime(this.startTime))
            );
            localeStartDate = new Date(localeStartDate.setHours(localeStartDate.getHours() - 8)).toString();
            let localeEndDate = new Date(
                Date.parse(this.endDate + "T" + this.convertTime(this.endTime))
            );
            localeEndDate = new Date(localeEndDate.setHours(localeEndDate.getHours() - 8)).toString();

            formData.append("localeEnd", localeEndDate);
            formData.append("localeStart", localeStartDate);

            axios
                .post(process.env.NUXT_ENV_BACKEND + "/addWorkshop", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                })
                .then((resp) => {
                    let message = resp.data;
                    this.snackbar = true;
                    this.snackbarMessage = message;
                    if (message == "success") {
                        setTimeout(() => this.$router.push({ path: "/app/workshop/main" }), 2000);
                    }
                })
                .catch((err) => {
                    console.log(err.data);
                });

            return;
        },
        getLatLng(dict) {
            this.lat = dict.lat;
            this.lng = dict.lng;
            console.log(this.lat);
            console.log(this.lng);
        },
    },

    mounted() {
        fetch(process.env.NUXT_ENV_BACKEND + "/getWorkshops")
            .then((resp) => {
                if (!resp.ok) {
                    throw Error(resp.statusText);
                }
                return resp;
            })
            .then((resp) => resp.json())
            .then((data) => {
                var tempSet = new Set();
                data.map((obj) => {
                    tempSet.add(obj.category);
                });
                this.categories = this.categories.concat(Array.from(tempSet));
            })
            .catch((err) => console.log("oops Workshops API is down", err));

        let currentDateTime = new Date();
        currentDateTime.setHours(currentDateTime.getHours() + 1);
        this.startTime = `${currentDateTime.getHours()}:${currentDateTime.getMinutes()}`;
        currentDateTime.setHours(currentDateTime.getHours() + 1);
        this.endTime = `${currentDateTime.getHours()}:${currentDateTime.getMinutes()}`;
    },
};
</script>

<style></style>
