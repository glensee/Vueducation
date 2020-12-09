<template>
    <v-navigation-drawer app clipped left permanent>
        <v-list>
            <v-list-item v-for="item in items" :key="item.index" :to="item.path">
                <v-list-item-icon>
                    <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
export default {
    data() {
        return {
            items: [
                { title: "Profile", path: "/account", icon: "mdi-account" },
                { title: "My Questions", path: "/questions", icon: "mdi-forum" },
                { title: "Achievements", path: "/achievements", icon: "mdi-trophy" },
            ],
            username: "Cliffen Lee",
        };
    },
};
</script>

<style>
.v-list-item-content {
    text-decoration: none;
}
</style>
