<template>
    <v-app>
        <AppHeader />
        <SideBarNav />
        <v-main>
            <nuxt />
        </v-main>
        <AppFooter />
    </v-app>
</template>

<script>
import AppHeader from "../components/AppHeader";
import AppFooter from "../components/AppFooter";
import SideBarNav from "../components/SideBarNav";

export default {
    head() {
        return {
            script: [
                {
                    src: `https://maps.googleapis.com/maps/api/js?key=${process.env.NUXT_ENV_GOOGLE_API}&region=SG&libraries=places`,
                },
            ],
        };
    },
    components: {
        AppHeader,
        AppFooter,
    },
    mounted() {},
    methods: {},
};
</script>

<style></style>
