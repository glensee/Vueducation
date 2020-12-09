<template>
    <div>
        <v-container fill-height fluid grid-list-xl id="topContainer">
            <v-layout justify-center wrap>
                <v-flex xs12 md8>
                    <v-form>
                        <v-container id="form">
                            <v-layout wrap>
                                <v-flex xs12 md4>
                                    <v-text-field
                                        :clearable="!readOnly"
                                        :outlined="readOnly"
                                        :class="['purple-input', readOnly ? 'disable-events' : '']"
                                        label="Occupation"
                                        :placeholder="occupation"
                                        v-model="occupation"
                                    />
                                </v-flex>
                                <v-flex xs12 md4>
                                    <v-text-field
                                        :clearable="!readOnly"
                                        :outlined="readOnly"
                                        label="First Name"
                                        :class="['purple-input', readOnly ? 'disable-events' : '']"
                                        :placeholder="firstname"
                                        v-model="firstname"
                                    />
                                </v-flex>
                                <v-flex xs12 md4>
                                    <v-text-field
                                        :clearable="!readOnly"
                                        :outlined="readOnly"
                                        label="Last Name"
                                        :class="['purple-input', readOnly ? 'disable-events' : '']"
                                        :placeholder="lastname"
                                        v-model="lastname"
                                    />
                                </v-flex>
                                <v-flex xs12>
                                    <v-text-field
                                        :clearable="!readOnly"
                                        :outlined="readOnly"
                                        :class="['purple-input', readOnly ? 'disable-events' : '']"
                                        label="About Me"
                                        :value="about"
                                        v-model="about"
                                    />
                                </v-flex>
                                <v-flex xs12 text-xs-right>
                                    <v-btn class="mr-10" tile @click="editMode()" width="180">
                                        <v-icon left>
                                            {{ primaryMdi }}
                                        </v-icon>
                                        {{ primaryButton }}
                                    </v-btn>
                                    <span v-if="readOnly"></span>
                                    <v-btn
                                        v-else
                                        tile
                                        color="success"
                                        @click="confirmChanges()"
                                        width="210"
                                    >
                                        <v-icon left>
                                            {{ secondaryMdi }}
                                        </v-icon>
                                        {{ secondaryButton }}
                                    </v-btn>
                                </v-flex>
                            </v-layout>
                        </v-container>
                    </v-form>
                </v-flex>
                <v-flex xs12 md3>
                    <v-card class="mx-auto" color="grey-lighten-5" tile>
                        <v-img
                            height="200"
                            src="https://cdn.vuetifyjs.com/images/cards/server-room.jpg"
                        ></v-img>

                        <v-list-item-avatar
                            class="d-flex align-center justify-center mx-auto mt-n16"
                            size="120"
                        >
                            <img :src="profilePic" alt="John" />
                        </v-list-item-avatar>
                        <v-card-title> </v-card-title>

                        <v-card-text class="">
                            <p id="preview" class="font-weight-bold subtitle-2 mb-3">
                                {{ username.toUpperCase() }}
                            </p>
                            <p id="preview" class="card-title font-weight-normal mb-3 overline">
                                {{ occupation }}
                            </p>
                            <p id="desc" class="card-description font-weight-light caption">
                                {{ about }}
                            </p>
                        </v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>

        <v-container fill-height fluid grid-list-xl id="btmContainer">
            <v-layout justify-center wrap>
                <v-flex xs12 md8 align-self-center>
                    <v-sheet tile height="54" class="d-flex">
                        <v-btn icon class="ma-2" @click="$refs.calendar.prev()">
                            <v-icon>mdi-chevron-left</v-icon>
                        </v-btn>
                        <v-select
                            v-model="type"
                            :items="types"
                            dense
                            outlined
                            hide-details
                            class="ma-2"
                        ></v-select>
                        <v-select
                            v-model="weekday"
                            :items="weekdays"
                            dense
                            outlined
                            hide-details
                            class="ma-2"
                        ></v-select>
                        <v-btn icon class="ma-2" @click="$refs.calendar.next()">
                            <v-icon>mdi-chevron-right</v-icon>
                        </v-btn>
                    </v-sheet>
                    <v-sheet height="600">
                        <v-calendar
                            ref="calendar"
                            v-model="value"
                            :weekdays="weekday"
                            :type="type.toLowerCase()"
                            :events="events"
                            :event-overlap-threshold="30"
                            :event-color="getEventColor"
                            @change="getEvents"
                        ></v-calendar>
                    </v-sheet>
                </v-flex>
                <v-flex xs12 md3 align-self-center>
                    <v-card class="mx-auto d-flex flex-col" max-width="100%" outlined>
                        <v-list-item three-line>
                            <v-list-item-content>
                                <div class="overline" id="achievements">
                                    <h2>ACHIEVEMENTS</h2>
                                </div>
                                <v-list-item-subtitle>You have</v-list-item-subtitle>
                                <v-list-item-title class="headline mb-1">
                                    {{ points }} points
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-card>

                    <v-card>
                        <v-carousel hide-delimiters height="auto">
                            <v-carousel-item
                                reverse-transition="fade-transition"
                                transition="fade-transition"
                                v-for="item in trophies"
                                :key="item"
                            >
                                <v-row class="fill-height pa=0" align="center" justify="center">
                                    <img :src="achievements[item].src" alt="trophy" />
                                </v-row>
                            </v-carousel-item>
                        </v-carousel>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
import { resolveConfig } from "prettier";

export default {
    head: {
        title: "Vueducation - Account",
    },
    components: {},
    middleware: ["auth"],
    data() {
        return {
            profilePic: require("../../assets/profile/" + this.$auth.user.image),
            primaryMdi: "mdi-pencil",
            secondaryMdi: "mdi-send",
            primaryButton: "Edit Profile",
            secondaryButton: "Confirm Changes",
            readOnly: true,
            occupation: this.$auth.user.occupation,
            username: this.$auth.user.username,
            firstname: this.$auth.user.first_name,
            lastname: this.$auth.user.last_name,
            email: this.$auth.user.email,
            about: this.$auth.user.about_me,
            points: this.$auth.user.points,
            trophies: [],
            achievements: [
                {
                    id: "1",
                    src: require("../../assets/trophies/gold-cup.png"),
                },
                {
                    id: "2",
                    src: require("../../assets/trophies/silver-cup.png"),
                },
                {
                    id: "3",
                    src: require("../../assets/trophies/bronze-cup.png"),
                },
                {
                    id: "4",
                    src: require("../../assets/trophies/empty.png"),
                },
            ],

            type: "Month",
            types: ["Month", "Week", "Day", "4day"],
            weekday: [0, 1, 2, 3, 4, 5, 6],
            weekdays: [
                { text: "Sun - Sat", value: [0, 1, 2, 3, 4, 5, 6] },
                { text: "Mon - Sun", value: [1, 2, 3, 4, 5, 6, 0] },
                { text: "Mon - Fri", value: [1, 2, 3, 4, 5] },
                { text: "Mon, Wed, Fri", value: [1, 3, 5] },
            ],
            value: "",
            events: [],
            colors: ["blue", "indigo", "deep-purple", "cyan", "green", "orange"],
        };
    },
    beforeMount() {
        const that = this;
        this.$axios
            .get("/api/numberOfBestAnswer/" + this.$auth.user.username)
            .then(function (response) {
                const bestCount = response.data.total;
                if (bestCount >= 7) {
                    that.trophies.push(0);
                    that.trophies.push(1);
                    that.trophies.push(2);
                } else if (bestCount >= 5) {
                    that.trophies.push(1);
                    that.trophies.push(2);
                } else if (bestCount >= 3) {
                    that.trophies.push(2);
                } else {
                    that.trophies.push(3);
                }
            });
    },
    methods: {
        editMode() {
            if (this.readOnly) {
                this.readOnly = false;
                this.primaryButton = "Return";
                this.primaryMdi = "mdi-keyboard-return";
            } else {
                this.occupation = this.$auth.user.occupation;
                this.firstname = this.$auth.user.first_name;
                this.lastname = this.$auth.user.last_name;
                this.about = this.$auth.user.about_me;
                this.readOnly = true;
                this.primaryButton = "Edit Profile";
                this.primaryMdi = "mdi-pencil";
            }
        },
        confirmChanges() {
            const data = {
                about_me: this.about,
                email: this.email,
                first_name: this.firstname,
                image: this.$auth.user.image,
                last_name: this.lastname,
                occupation: this.occupation,
                points: this.points,
                user_id: this.$auth.user.user_id,
                username: this.username,
            };

            const that = this;
            this.$axios
                .put("/api/users/" + this.$auth.user.username, data)
                .then(function (response) {
                    that.afterChange();
                });
        },
        afterChange() {
            this.readOnly = true;
            this.primaryButton = "Edit Profile";
            this.primaryMdi = "mdi-pencil";
        },
        getEvents({ start, end }) {
            let formData = new FormData();
            formData.append("user", this.$auth.user.username);
            const that = this;

            this.$axios.post("/api/getcalendar", formData).then(function (response) {
                const resp = response.data;
                const events = [];
                console.log(resp)
                for (var item of resp) {
                    console.log("before first: " + item.name + " " + item.start)
                    var tempFirst = new Date(item.start)
                    var first = tempFirst.setHours(tempFirst.getHours() + (8));
                    console.log("after first: " + new Date(first))


                    console.log("before second: " + item.end)
                    var tempSecond = new Date(item.end)
                    var second = tempSecond.setHours(tempSecond.getHours() + (8));
                    console.log("after second: " + new Date(second))

                    events.push({
                        name: item.name,
                        start: new Date(item.start),
                        end: new Date(item.end),
                        color: that.colors[0],
                        timed: !item.allDay,
                    });
                }

                that.events = events;
            });
        },
        getEventColor(event) {
            return event.color;
        },
    },
};
</script>

<style>
#topContainer {
    margin-top: 4%;
}

#preview {
    text-align: center;
}

#desc {
    text-align: center;
}

.disable-events {
    pointer-events: none;
}
</style>
