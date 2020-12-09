<template>
    <div class="mb-5">
        <div style="width: 90%; margin: auto" v-if="!loading">
            <span class="text-h2 py-4 font-weight-medium">{{ workshopInfo.title }}</span>
            <span class="text-h3 py-4 mb-3">{{ workshopInfo.institution }}</span>
            <div v-if="workshopInfo.mode == 'online'">
                <client-only>
                    <div style="text-align: center">
                        <youtube
                            :video-id="workshopInfo.link.split('?')[1].split('=')[1]"
                        ></youtube>
                    </div>
                </client-only>
            </div>

            <div v-if="workshopInfo.startDate != workshopInfo.endDate">
                <span class="body-1 mt-5"
                    ><strong>Start Date: </strong>{{ workshopInfo.startDate }}
                </span>
                <span class="body-1 mt-5"
                    ><strong>Start Time: </strong>{{ workshopInfo.startTime }}
                </span>
                <span class="body-1 mt-5"
                    ><strong>End Date: </strong>{{ workshopInfo.endDate }}
                </span>
                <span class="body-1 mt-5"
                    ><strong>End Time: </strong>{{ workshopInfo.endTime }}
                </span>
            </div>

            <div v-if="workshopInfo.startDate == workshopInfo.endDate">
                <span class="body-1 mt-5"
                    ><strong>Date: </strong>{{ workshopInfo.startDate }}
                </span>
                <span class="body-1 mt-5"
                    ><strong>Start Time: </strong>{{ workshopInfo.startTime }}
                </span>
                <span class="body-1 mt-5"
                    ><strong>End Time: </strong>{{ workshopInfo.endTime }}
                </span>
            </div>
            <span class="body-1 mt-5"
                ><strong>Description: </strong>{{ workshopInfo.description }}
            </span>
        </div>

        <div style="width: 90%; margin: auto" v-if="loading == false" class="mt-5">
            <v-btn
                :href="this.createGoogleLink()"
                target="_blank"
                class="mr-5 mb-3"
                @click="() => markCalendar()"
                >GOOGLE CALendar</v-btn
            >
            <v-btn
                :href="this.createOutlookLink()"
                target="_blank"
                class="mr-5 mb-3"
                @click="() => markCalendar()"
                >Outlook CALendar</v-btn
            >
            <v-btn
                :href="this.createYahooLink()"
                target="_blank"
                class="mr-5 mb-3"
                @click="() => markCalendar()"
                >YAHOO CALendar</v-btn
            >
        </div>

        <span
            id="gmap"
            style="height: 400px; width: 90%; margin: auto; margin-top: 32px; margin-bottom: 32px"
            :class="loading == false && workshopInfo.mode == 'online' ? 'hide-map' : ''"
        ></span>

        <v-snackbar v-model="snackbar">
            {{ snackbarMessage }}
            <v-btn text color="primary" @click.native="snackbar = false">Close</v-btn>
        </v-snackbar>
    </div>
</template>

<script>
import axios from "axios";

export default {
    components: {
        axios,
    },

    middleware: ["auth"],

    data() {
        return {
            loading: true,
            id: this.$route.params.id,
            workshops: [],
            workshopInfo: {},
            snackbar: false,
            snackbarMessage: "",
        };
    },
    head() {
        return {
            title: `Vueducation - ${this.workshopInfo.title}`,
        };
    },
    methods: {
        refreshMap() {
            var myLatLng = {
                lat: parseFloat(this.workshopInfo.location.split(",")[0]),
                lng: parseFloat(this.workshopInfo.location.split(",")[1]),
            };

            console.log(myLatLng);

            var map = new google.maps.Map(document.getElementById("gmap"), {
                zoom: 17,
                center: myLatLng,
            });

            var marker = new google.maps.Marker({
                position: myLatLng,
                map,
                title: "Workshop location",
            });
        },

        markCalendar() {
            let formData = new FormData();
            formData.append("name", this.workshopInfo.title);
            formData.append("user", this.$auth.user.username);
            formData.append("start", this.workshopInfo.localeStart);
            formData.append("end", this.workshopInfo.localeEnd);

            axios
                .post(process.env.NUXT_ENV_BACKEND + "/markcalendar", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                })
                .then((resp) => {
                    let message = resp.data;
                    this.snackbar = true;
                    this.snackbarMessage = message;
                })
                .catch((err) => {
                    console.log(err.data);
                });
        },

        createGoogleLink() {
            var url = `https://www.google.com/calendar/render?action=TEMPLATE&text=${
                this.workshopInfo.title
            }&details=${this.workshopInfo.link + this.workshopInfo.description}&location=${
                this.workshopInfo.location
            }&dates=${this.workshopInfo.icalStart}%2F${this.workshopInfo.icalEnd}`;
            return url;
        },

        createOutlookLink() {
            var url = `https://outlook.live.com/owa/?path=%2Fcalendar%2Faction%2Fcompose&rru=addevent&startdt=${this.workshopInfo.icalStart.slice(
                0,
                -1
            )}&enddt=${this.workshopInfo.icalEnd.slice(0, -1)}&subject=${
                this.workshopInfo.title
            }&body=${this.workshopInfo.link + this.workshopInfo.description}&location=${
                this.workshopInfo.location
            }`;
            return url;
        },

        createYahooLink() {
            var url = `https://calendar.yahoo.com/?v=60&title=${this.workshopInfo.title}&st=${
                this.workshopInfo.icalStart
            }&et=${this.workshopInfo.icalEnd}&desc=${
                this.workshopInfo.link + this.workshopInfo.description
            }&in_loc=${this.workshopInfo.location}`;

            return url;
        },
    },

    mounted() {
        const root = this;
        fetch(process.env.NUXT_ENV_BACKEND + "/getWorkshops")
            .then((resp) => {
                if (!resp.ok) {
                    throw Error(resp.statusText);
                }
                return resp;
            })
            .then((resp) => resp.json())
            .then((data) => {
                this.workshops = data;
                var tempSet = new Set();
                for (var thing of data) {
                    tempSet.add(thing.category);
                    if (thing.index == this.id) {
                        this.workshopInfo = thing;
                    }
                }
                this.categories = Array.from(tempSet);
                this.loading = false;
                root.refreshMap();
            })
            .catch((err) => console.log("oops Workshops API is down", err));
    },
};
</script>

<style>
.hide-map {
    display: none;
}
iframe {
    width: 90vw;
}
</style>
