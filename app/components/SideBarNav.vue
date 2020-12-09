<template>
    <div class="sidenav-container">
        <div class="backdrop" v-if="isSideBar" @click="toggle"></div>
        <v-navigation-drawer
            v-if="isSideBar"
            v-model="isSideBar"
            absolute
            left
            temporaryw
            hide-overlay
            style="position: fixed"
        >
            <v-list nav dense>
                <v-list-item-group>
                    <v-list-item href="/app/workshop/main">
                        <v-list-item-title>Workshop</v-list-item-title>
                    </v-list-item>

                    <v-list-item href="/app/redeem">
                        <v-list-item-title>Redeem</v-list-item-title>
                    </v-list-item>

                    <v-list-item href="/app/donate">
                        <v-list-item-title>Donate</v-list-item-title>
                    </v-list-item>

                    <v-list-item href="/app/chat">
                        <v-list-item-title>Chat</v-list-item-title>
                    </v-list-item>

                    <v-list-item href="/app/account">
                        <v-list-item-title>Account</v-list-item-title>
                    </v-list-item>

                    <v-list-item @click="this.toggleDarkMode">
                        <v-list-item-title>{{
                            this.$vuetify.theme.dark == true ? "Light Mode" : "Dark Mode"
                        }}</v-list-item-title>
                    </v-list-item>

                    <v-list-item
                        v-if="$auth.loggedIn"
                        @click="
                            $auth.logout();
                            close();
                        "
                    >
                        <v-list-item-title>Log Out</v-list-item-title>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";

export default {
    computed: {
        isSideBar: {
            get() {
                return this.$store.getters["sideBarNav/getToggleSideBar"];
            },
            set() {},
        },
    },

    methods: {
        toggleDarkMode() {
            if (process.browser) {
                this.$vuetify.theme.dark = !(localStorage.getItem("darkMode") === "true");
                localStorage.setItem("darkMode", !(localStorage.getItem("darkMode") === "true"));
            }
        },
        ...mapMutations({
            toggle: "sideBarNav/toggle",
            close: "sideBarNav/close",
        }),
    },
};
</script>

<style lang="scss" scoped>
.backdrop {
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    z-index: 1000;
    position: fixed;
    top: 0;
    left: 0;
}

.v-navigation-drawer {
    z-index: 1050;
}
</style>
