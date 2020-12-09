<template>
    <v-footer>
        <v-container fluid>
            <v-layout>
                <v-flex />
                <v-row>
                    <v-flex md8>
                        <v-col>
                            <h3>About</h3>
                            <p class="text-justify font-weight-light">
                                Vueducation is your go to website to ask and answer questions from
                                all around the world. Need to get your questions answered? Simply
                                snap a photo of your homework, upload it and check your answer. Not
                                only that, there is a multitude of workshops for you to attend
                                and/or host. Collect points by helping others and hosting workshops
                                to redeem a wide variety of vouchers and credits.
                            </p>
                        </v-col>
                    </v-flex>
                    <v-col>
                        <h3>Connect with us</h3>
                        <a
                            href="https://www.instagram.com/twicetagram/"
                            class="text-decoration-none"
                            ><v-icon class="pink--text text--lighten--2">mdi-instagram</v-icon></a
                        >
                        <a href="https://www.facebook.com/JYPETWICEg" class="text-decoration-none"
                            ><v-icon class="indigo--text text--darken--3">mdi-facebook</v-icon></a
                        >
                        <a
                            href="https://www.linkedin.com/in/tzu-yu-wang-77582711/"
                            class="text-decoration-none"
                            ><v-icon class="blue--text">mdi-linkedin</v-icon></a
                        >
                    </v-col>
                </v-row>
                <v-flex md1 />
            </v-layout>
        </v-container>
    </v-footer>
</template>

<script>
export default {
    name: "AppFooter",
};
</script>

<style>
span {
    display: block;
}
</style>
