<template>
    <v-btn depressed @click="this.toggleDarkMode">
        <v-icon> mdi-brightness-6 </v-icon>
    </v-btn>
</template>

<script>
export default {
    methods: {
        toggleDarkMode() {
            if (process.browser) {
                this.$vuetify.theme.dark = !(localStorage.getItem("darkMode") === "true");
                localStorage.setItem("darkMode", !(localStorage.getItem("darkMode") === "true"));
            }
        },
    },
};
</script>

<style></style>
