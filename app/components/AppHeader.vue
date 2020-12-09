<template>
    <v-app-bar app>
        <v-app-bar-nav-icon class="hidden-lg-and-up" @click="toggle"></v-app-bar-nav-icon>
        <span
            @click="$router.push('/app')"
            class="display-1 text-uppercase font-weight-light"
            style="cursor: pointer"
            >Vueducation</span
        >
        <template>
            <v-tabs right :hide-slider="true" class="hidden-md-and-down">
                <v-tab to="/app/workshop/main"> Workshop </v-tab>

                <v-tab to="/app/redeem"> Redeem </v-tab>

                <v-tab to="/app/donate"> Donate </v-tab>

                <v-tab to="/app/chat"> Chat </v-tab>

                <v-tab to="/app/account">
                    {{ this.$auth.user == null ? "Account" : this.$auth.user.username }}
                </v-tab>
            </v-tabs>

            <v-toolbar-items class="hidden-md-and-down">
                <DarkModeButton />
                <v-btn
                    v-if="$auth.loggedIn"
                    @click="
                        $auth.logout();
                        close();
                    "
                    color="primary"
                >
                    <span>Log Out</span>
                </v-btn>

                <v-btn v-else href="/app/login" color="primary">
                    <span>Log In</span>
                </v-btn>
            </v-toolbar-items>
        </template>
    </v-app-bar>
</template>

<script>
import DarkModeButton from "./DarkModeButton";
import { mapMutations } from "vuex";

export default {
    name: "AppHeader",
    components: {
        DarkModeButton,
    },
    methods: {
        ...mapMutations({
            toggle: "sideBarNav/toggle",
            close: "sideBarNav/close",
        }),
    },
};
</script>

<style>
span {
    font-family: Arial, Helvetica, sans-serif;
}

.disable-select {
    user-select: none; /* supported by Chrome and Opera */
    -webkit-user-select: none; /* Safari */
    -khtml-user-select: none; /* Konqueror HTML */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
    font-size: 30px;
}
</style>
